# -*- coding: utf-8 -*- 

# This program source code file is part of KiCad, a free EDA CAD application.
#
# Copyright (C) 2015 Torsten Hueter, torstenhtr@gmx.de
# Copyright (C) 2015 KiCad Developers, see CHANGELOG.TXT for contributors.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, you may find one here:
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# or you may search the http://www.gnu.org website for the version 2 license,
# or you may write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import math
import pcbnew
import random

# TODO Tented Vias


class StitchVia(object):

    def __init__(self, board):
        '''
        Creates the via as pad for stitching.
        :param board: is the associated board.
        '''
        self.module = pcbnew.MODULE(board)
        self.pad = pcbnew.D_PAD(self.module)

        # default via properties
        self.textscale = 0.2                # Scaling factor for the text (Reference)
        self.via_diameter = 600000          # Via via_diameter in [BIU]
        self.drill_diameter = 300000        # Drill size in [BIU]
        self.solder_mask_margin = -100000   # The solder mask margin
        self.clearance = 250000             # Local clearance of the pad
        
        self.isTented = False

        #self.pad.SetSize(pcbnew.wxSize(self.via_diameter, self.via_diameter))
        #self.pad.SetDrillSize(
        #    pcbnew.wxSize(self.drill_diameter, self.drill_diameter))
        self.pad.SetShape(pcbnew.PAD_CIRCLE)
        self.pad.SetAttribute(pcbnew.PAD_ATTRIB_STANDARD)
        self.pad.SetLayerSet(pcbnew.D_PAD.StandardMask())
        self.pad.SetZoneConnection(pcbnew.PAD_ZONE_CONN_FULL)
        self.pad.SetPos(pcbnew.wxPoint(0, 0))
        self.module.Add(self.pad)
        self.module.Reference().SetVisible(False)        
        self.module.Value().SetVisible(False)
        self.module.SetPosition(pcbnew.wxPoint(0, 0))

    @property
    def position(self):
        return self.module.GetPosition()
    
    @position.setter
    def position(self, point):
        self.pad.SetPos(pcbnew.wxPoint(0, 0))
        self.module.SetPosition(point)

    @property
    def via_diameter(self):
        return self._via_diameter
    
    @via_diameter.setter
    def via_diameter(self, diameter):
        self._via_diameter = diameter
        self.pad.SetSize(pcbnew.wxSize(diameter, diameter))

    @property
    def drill_diameter(self):
        return self._drill_diameter
    
    @drill_diameter.setter
    def drill_diameter(self, diameter):
        self._drill_diameter = diameter
        self.pad.SetDrillSize(
            pcbnew.wxSize(diameter, diameter))
        
    @property
    def reference(self):
        return self.module.GetReference()

    @reference.setter
    def reference(self, refDes):
        self.module.SetReference(refDes)

    @property
    def netcode(self):
        return self.pad.GetNetCode()

    @netcode.setter
    def netcode(self, netcode):
        self.pad.SetNetCode(netcode)

    @property
    def timestamp(self):
        self.module.GetTimeStamp()

    @property
    def clearance(self):
        return self.pad.GetLocalClearance()

    @clearance.setter
    def clearance(self, clearance):
        self.pad.SetLocalClearance(clearance)

    @property
    def solder_mask_margin(self):
        return self.pad.GetLocalSolderMaskMargin()

    @solder_mask_margin.setter
    def solder_mask_margin(self, margin):
        self.pad.SetLocalSolderMaskMargin(margin)

    @timestamp.setter
    def timestamp(self, timestamp):
        self.module.SetTimeStamp(timestamp)

    def adjustTextSize(self):
        # Adjust the text size to the via diameter
        self.module.Reference().SetHeight(int(self.via_diameter * self.textscale))
        self.module.Reference().SetWidth(int(self.via_diameter * self.textscale))
        self.module.Reference().SetThickness(int(self.via_diameter * self.textscale * 0.1))

    def copy_properties(self, via):
        '''
        Copies the stitch via properties from a given input via.
        :param via: is the input via.
        '''
        self.via_diameter = via.via_diameter
        self.drill_diameter = via.drill_diameter
        self.solder_mask_margin = via.solder_mask_margin
        self.clearance = via.clearance

class ViaStitching(object):

    '''
    This is the main class for via stitching of PCB boards.
    '''
    via_spacing = 2000000  # Via  spacing in [BIU]

    max_via_distance = 0    # Maximum distance from the outline

    # Grid
    grid_size = pcbnew.wxPoint(5000000, 5000000)  # Size of the grid in [BIU]
    grid_origin = pcbnew.wxPoint(0, 0)            # Origin of the grid in [BIU]

    # Determines, if the vias should be put on staggered rows
    is_staggered_rows = True

    # Should objects of the same net be stitched?
    is_stitching_same_net = False

    # Using of the netclass values for the given zone
    is_use_netclass_values = True

    # Snap the VIAs to the current grid
    is_align_to_grid = False

    # That's the reference to the board
    board = None

    # Additional constraint area for the vias
    constraint_area = None

    # Random offset factor in [%]
    random_offset_factor = 0

    # Distance for edge stitching
    edge_distance = 1000000

    # Used for the UNDO operations
    item_picker = pcbnew.ITEM_PICKER()
    picked_items = pcbnew.PICKED_ITEMS_LIST()

    # P&S router is used for collision testing
    router = pcbnew.PNS_ROUTER()

    # Prefix for the RefDes of the via
    prefix = u"VS"

    def __init__(self):
        '''
        Constructor of the class.
        '''
        # That's the reference via for all stitched vias
        self.referenceVia = StitchVia(self.board)

    @property
    def grid_size(self):
        screen = pcbnew.GetPcbScreen()
        return pcbnew.GetGridSize(screen)

    @property
    def grid_origin(self):
        return pcbnew.GetBoard().GetGridOrigin()

    @property
    def board(self):
        return pcbnew.GetBoard()

    @property
    def view(self):
        return pcbnew.GetToolManager().GetView()

    def _snap_to_grid(self, point):
        '''
        Snaps a given point to the current grid.
        :param point: is the point to be snapped. 
        :return: the snapped point.
        '''

        offsetx = (point.x - self.grid_origin.x) % self.grid_size.x
        point.x -= offsetx
        if offsetx >= self.grid_size.x / 2:
            point.x += self.grid_size.x

        offsety = (point.y - self.grid_origin.y) % self.grid_size.y
        point.y -= offsety
        if offsety >= self.grid_size.y / 2:
            point.y += self.grid_size.y

        return point

    @property
    def selected_zone(self):
        '''
        Get the currently selected zone or return None if no zone was selected.
        :return: the selected zone.
        '''
        toolmanager = pcbnew.GetToolManager()
        currenttool = toolmanager.GetCurrentTool()
        if currenttool.GetName() != "pcbnew.PointEditor":
            return None
        else:
            pointeditor = pcbnew.Cast_to_POINT_EDITOR(currenttool)
            item = pointeditor.GetEditParent()
            if (item.GetClass() != u'ZONE_CONTAINER'):
                return None
            else:
                boarditem = pcbnew.Cast_to_BOARD_ITEM(item)
                zone = boarditem.Cast_to_ZONE_CONTAINER()
                return zone

    def add_constraint_area(self):
        '''
        Add the currently selected zone for the constraint area or set to None if no zone was selected.
        '''
        self.constraint_area = self.selected_zone

    def _compute_stitch_bb(self, zone):
        '''
        Computes the bounding box for via stitching.
        :param zone: is the zone for stitching.
        '''
        zone_bb = zone.GetBoundingBox()
        stitch_bb = []

        start_point = zone_bb.GetOrigin()
        end_point = zone_bb.GetEnd()

        if self.is_align_to_grid:
            start_point = self._snap_to_grid(start_point)
            end_point = self._snap_to_grid(end_point)

        stitch_bb.append(start_point.x - self.via_spacing / 2)
        stitch_bb.append(end_point.x + self.via_spacing / 2)
        stitch_bb.append(start_point.y - self.via_spacing / 2)
        stitch_bb.append(end_point.y + self.via_spacing / 2)

        return stitch_bb

    def _compute_random_offset(self):
        '''
        Computes a random offset for the via placement.
        :return: the random offset.
        '''
        if self.random_offset_factor > 0:
            x = self.via_spacing * (self.random_offset_factor / 100.0)
            return random.randint(-x, x)
        else:
            return 0

    def _distance(self, pointA, pointB):
        '''
        Get the distance between two points.
        :param pointA: is the first point.
        :param pointB: is the second point.
        '''
        return math.sqrt((pointA - pointB).x ** 2 + (pointA - pointB).y ** 2)

    def _sync_router(self):
        '''
        Syncronizes the P&S Router.
        '''
        self.router.SetBoard(self.board)
        self.router.SyncWorld()

    def _compute_identifier(self):
        '''
        Iterates over the list of the board modules and determines 
        the identifier for the next stitching vias. 
        '''
        largest_identifier = 0
        for module in self.board.GetModules():
            refdes = str(module.GetReference())
            if refdes.startswith(self.prefix):
                try:
                    remainder = int(refdes.lstrip(self.prefix))
                except:
                    remainder = 0
                largest_identifier = max(remainder, largest_identifier)
        return largest_identifier + 1

    def _add_via(self, via_position, identifier):
        '''
        Adds the via to the board.
        :param via_position: is a 2D-vector of the via position.
        :param identifier: is the identifier of the via.
        :return: True, if the via was placed, else False.
        '''

        # Dummy obstacle vector
        obs = pcbnew.ObstacleVector()

        if self.is_align_to_grid:
            via_position = self._snap_to_grid(via_position)

        self.referenceVia.pad.SetPos(via_position)
        solid = self.router.CreateSolidFromPad(self.referenceVia.pad)

        if not self.is_stitching_same_net:
            solid.SetNet(-1)

        # Determine the distance from the zone outline
        via_distance = self.outline.Distance(via_position, True)

        # If a constraint area was specified, compute the distance to that area
        # as well
        if self.constraint_area is not None:
            d = self.constraint_area.Outline().Distance(via_position, True)
            via_distance = min(via_distance, d)

        # We're checking, if it's possible to set the via at the given position
        if via_distance > self.referenceVia.via_diameter / 2:
            is_feasible_distance = (self.max_via_distance == 0 or
                                    (via_distance < self.max_via_distance)) and \
                via_distance > self.referenceVia.via_diameter / 2
            if is_feasible_distance:
                w = self.router.GetWorld()
                # Collision check
                if w.QueryColliding(solid, obs) == 0:
                    # Create the via and add it to the board
                    stitchvia = StitchVia(self.board)
                    stitchvia.copy_properties(self.referenceVia)
                    stitchvia.reference = self.prefix + str(identifier)
                    stitchvia.position = via_position
                    stitchvia.netcode = self.netcode
                    stitchvia.timestamp = self.selected_zone.GetTimeStamp()
                    stitchvia.clearance = 0
                    self.view.AddNative(stitchvia.module)
                    stitchvia.adjustTextSize()
                    stitchvia.module.ViewUpdate(stitchvia.module.ALL)
                    self.board.Add(stitchvia.module)
                    self.picked_items.PushItem(
                        pcbnew.ITEM_PICKER(stitchvia.module))
                    return True
        return False

    def stitch_edge_generator(self):
        '''
        Stitch the zone edge only, yields after every edge stitching.
        '''
        if self.selected_zone is None:
            raise RuntimeError("No zone was selected!")

        # Determine a stitchpolyline for stitching the zone edge
        self.outline = self.selected_zone.Outline()
        polyset = pcbnew.SHAPE_POLY_SET()

        # Create a deflated polygon for stitching of the zone edge
        self.selected_zone.TransformOutlinesShapeWithClearanceToPolygon(polyset,
                                                                        -self.edge_distance,
                                                                        False)
        for j in range(polyset.OutlineCount()):
            
            stitchpolyline = polyset.Outline(j)
            stitchpolyline.Append(stitchpolyline.Point(0))
            self.netcode = self.selected_zone.GetNetCode()
            corners = stitchpolyline.PointCount()

            # Now iterate over the edge list and place vias along these edges
            if corners > 1:
                self._sync_router()
                self.picked_items.ClearItemsList()
                start = pcbnew.wxPoint(
                    stitchpolyline.Point(0).x, stitchpolyline.Point(0).y)
                firstPoint = start
                lastPoint = start
                j = self._compute_identifier()
                t = 0.0
                for i in range(1, corners):
                    end = pcbnew.wxPoint(
                        stitchpolyline.Point(i).x, stitchpolyline.Point(i).y)

                    dist = self._distance(start, end)
                    if dist > 0.0:
                        deltat = 1.0 / (dist / self.via_spacing)
                        while t <= 1.0:
                            via_position = pcbnew.wxPoint(start.x + t * float(end.x - start.x),
                                                          start.y + t * float(end.y - start.y))
                            is_feasible = (via_position == firstPoint or
                                           (via_position != firstPoint and
                                            self._distance(firstPoint, via_position) >= self.via_spacing and
                                            self._distance(lastPoint, via_position) >= self.via_spacing - 1))
                            if is_feasible:
                                if self._add_via(via_position, j):
                                    lastPoint = via_position
                                    j += 1
                            t += deltat
                        start = end
    
                        if t >= 1.0:
                            t -= 1.0
                        else:
                            t = 0.0
                    progress = int((100.0 * i) / corners)
                    yield progress
    
                # Add vias to the  undo list
                pcbnew.OnModify()
                pcbnew.SaveCopyInUndoList(
                    self.picked_items, pcbnew.UR_NEW, pcbnew.wxPoint(0, 0))
    
                # FIXME module->RunOnChildren is not usable in Python, this should be encapsulated
                # Thus we're redrawing the full board via a helper method
                pcbnew.RedrawGalCanvas()
                yield 100

    def stitch_zone_generator(self):
        '''
        Stitch a selected zone, yields after every row stitching.
        '''
        # Get the zone for stitching
        zone = self.selected_zone
        if zone is None:
            raise RuntimeError("No zone was selected!")

        # Get the zone outline and its bounding box
        self.outline = zone.Outline()
        self.netcode = zone.GetNetCode()

        self._sync_router()
        self.picked_items.ClearItemsList()

        stitch_bb = self._compute_stitch_bb(zone)

        # Now we know the limits and use two loops to set the vias
        row = 0
        i = self._compute_identifier()
        for y in range(stitch_bb[2], stitch_bb[3], self.via_spacing):
            start = stitch_bb[0]
            stop = stitch_bb[1]
            if self.is_staggered_rows and row % 2 == 1:
                start -= self.via_spacing / 2
                stop += self.via_spacing / 2
            for x in range(start, stop, self.via_spacing):
                via_position = pcbnew.wxPoint(x + self._compute_random_offset(),
                                              y + self._compute_random_offset())
                if self._add_via(via_position, i):
                    i += 1
            row += 1
            # Yield here the stitching, that the caller can update the progress
            # bar
            maxy = float(stitch_bb[3] - stitch_bb[2])
            progress = 100 if maxy == 0 else int(
                float(y - stitch_bb[2]) / maxy * 100.0)
            yield progress

        # Add vias to undo
        pcbnew.OnModify()
        pcbnew.SaveCopyInUndoList(
            self.picked_items, pcbnew.UR_NEW, pcbnew.wxPoint(0, 0))

        # FIXME module->RunOnChildren is not usable for Python, this should be encapsulated
        # This we're redrawing the full board via a helper method'
        pcbnew.RedrawGalCanvas()

        yield 100

    def stitch_zone(self):
        '''
        Stitch the selected zone.
        '''
        print "Stitch zone .."
        for progress in self.stitch_zone_generator():
            print str(progress) + "% finished."

    def stitch_edge(self):
        '''
        Stitch the edge of the selected zone.
        '''
        print "Stitch edge .."
        for progress in self.stitch_edge_generator():
            print str(progress) + "% finished."

    def delete_vias(self, timestamp=None):
        '''
        Deletes all stitched vias. If a zone was selected - deletes only vias inside that zone.
        :param timestamp: is the timestamp filter for the vias to be deleted. 
        '''

        outline = None
        if self.selected_zone is not None:
            outline = self.selected_zone.Outline()

        for module in self.board.GetModules():
            refdes = str(module.GetReference())
            if refdes.startswith(self.prefix) and (timestamp is None or timestamp == module.GetTimeStamp()):
                if outline is None:
                    self.board.Delete(module)
                else:
                    if outline.Distance(module.GetPosition(), True) > 0:
                        self.board.Delete(module)
        pcbnew.RedrawGalCanvas()

    def save_vias(self):
        '''
        Save the stitched vias of the actual board.
        :return: the saved vias list. 
        '''
        saved_vias = []
        for module in self.board.GetModules():
            refdes = str(module.GetReference())
            if refdes.startswith(self.prefix):
                via = module.Duplicate()
                saved_vias.append(via)
        return saved_vias

    def restore_vias(self, saved_vias):
        '''
        Restore vias saved by the method save_vias() 
        :param saved_vias: the saved vias list.
        '''

        for via in saved_vias:
            refdes = str(via.GetReference())
            if refdes.startswith(self.prefix):
                self.board.Add(via)
        pcbnew.RedrawGalCanvas()
