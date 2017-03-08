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

from decimal import Decimal, getcontext
import via_stitching
from via_stitching_dialog_base import ViaStitchingDialogBase
import wx
import pcbnew

import gettext
_ = gettext.gettext

# Implementing ViaStitchingDialogBase


class ViaStitchingDialog(ViaStitchingDialogBase):

    def __init__(self, parent):
        ViaStitchingDialogBase.__init__(self, parent)
        self.viastitching = via_stitching.ViaStitching()

        # Determine the current unit
        self.isMetric = 'mm' in pcbnew.ReturnUnitSymbol()

        # Set the decimal precisuin
        getcontext().prec = 6

        self._update_via_properties()

        # Update text fields with the correct unit
        self._update_unit_text()

    def _mm_to_biu(self, mm):
        '''
        Converts the given value in [mm] to the board internal unit.
        :param mm: is the value in [mm].
        '''
        return int(mm * Decimal(pcbnew.IU_PER_MM))

    def _biu_to_mm(self, biu):  # @DontTrace
        '''
        Converts the value in board internal units to [mm].
        :param biu: is the value in BIU.
        '''
        return Decimal(biu) / Decimal(pcbnew.IU_PER_MM)

    def _biu_to_inch(self, biu):
        '''
        Converts the value in board internal units to [inch].
        :param biu: is the value in BIU.
        '''
        return Decimal(biu) / Decimal(pcbnew.IU_PER_MILS) / Decimal(1000)

    def _inch_to_biu(self, inch):
        '''
        Converts the given value in [inch] to the board internal unit.
        :param mm: is the value in [inch].
        '''
        return int(inch * Decimal(pcbnew.IU_PER_MILS) * 1000)

    def _from_biu(self, value):
        '''
        Converts the value in board internal units to the actual board unit.
        :param biu: is the value in BIU.
        '''
        if self.isMetric:
            return self._biu_to_mm(value)
        else:
            return self._biu_to_inch(value)

    def _to_biu(self, value):
        '''
        Converts the value from the actual board unit the board internal unit.
        :param value: is the value [actual board unit].
        '''
        if self.isMetric:
            return self._mm_to_biu(value)
        else:
            return self._inch_to_biu(value)

    def _add_label_text(self, label, text):
        label.SetLabelText(label.GetLabelText() + text)

    def _update_unit_text(self):
        unit = pcbnew.ReturnUnitSymbol()
        self._add_label_text(self.m_staticTextDrillDiameter, unit)
        self._add_label_text(self.m_staticTextEdgeDistance, unit)
        self._add_label_text(self.m_staticTextSolderMaskMargin, unit)
        self._add_label_text(self.m_staticTextViaDiameter, unit)
        self._add_label_text(self.m_staticTextViaSpacing, unit)

    def _update_via_properties(self):
        refvia = self.viastitching.referenceVia
        self.m_textCtrlDrillDiameter.SetValue(
            str(self._from_biu(refvia.drill_diameter)))
        self.m_textCtrlViaDiameter.SetValue(
            str(self._from_biu(refvia.via_diameter)))
        self.m_textCtrlSolderMaskMargin.SetValue(
            str(self._from_biu(refvia.solder_mask_margin)))
        self.m_textCtrlViaSpacing.SetValue(
            str(self._from_biu(self.viastitching.via_spacing)))
        self.m_textCtrlRandomOffset.SetValue(
            str(self._from_biu(self.viastitching.random_offset_factor)))
        self.m_textCtrlEdgeDistance.SetValue(
            str(self._from_biu(self.viastitching.edge_distance)))
        self._show_via_margin()
        self._show_stitch_edge()
        self._show_random_offset()

    def _show_via_margin(self):
        if self.viastitching.referenceVia.isTented:
            self.m_staticTextSolderMaskMargin.Disable()
            self.m_textCtrlSolderMaskMargin.Disable()
        else:
            self.m_staticTextSolderMaskMargin.Enable()
            self.m_textCtrlSolderMaskMargin.Enable()
            refvia = self.viastitching.referenceVia
            self.m_textCtrlSolderMaskMargin.SetValue(
                str(self._from_biu(refvia.solder_mask_margin)))

    def _show_stitch_edge(self):
        if self.m_checkStitchEdge.GetValue():
            self.m_staticTextEdgeDistance.Enable()
            self.m_textCtrlEdgeDistance.Enable()
        else:
            self.m_staticTextEdgeDistance.Disable()
            self.m_textCtrlEdgeDistance.Disable()

    def _show_random_offset(self):
        if self.m_checkRandomize.GetValue():
            self.m_labelRandomOffset.Enable()
            self.m_textCtrlRandomOffset.Enable()
        else:
            self.m_labelRandomOffset.Disable()
            self.m_textCtrlRandomOffset.Disable()

    def OnTentedViasCheckBox(self, event):
        self.viastitching.referenceVia.isTented = self.m_checkBoxTentedVias.GetValue()
        self._show_via_margin()

    def OnGetNetclassValuesButtonClick(self, event):
        if self.viastitching.selected_zone is not None:
            nc = self.viastitching.selected_zone.GetNetClass()
            self.viastitching.referenceVia.via_diameter = nc.GetViaDiameter()
            self.viastitching.referenceVia.drill_diameter = nc.GetViaDrill()
            self._update_via_properties()

    def OnStaggeredRowsCheckBox(self, event):
        self.viastitching.is_staggered_rows = self.m_checkBoxStaggeredRows.GetValue()

    def OnStitchEdgesCheckBox(self, event):
        self._show_stitch_edge()

    def OnRandomizeCheckBox(self, event):
        self._show_random_offset()

    def _checkValues(self):
        '''
        This method checks the user input, raises a value error if the input is invalid or
        starts the stitching, if all values are feasible.   
        '''
        try:
            drill_diameter = self._to_biu(
                Decimal(self.m_textCtrlDrillDiameter.GetValue()))
        except:
            raise ValueError(_("Invalid number for the drill diameter."))

        try:
            via_diameter = self._to_biu(
                Decimal(self.m_textCtrlViaDiameter.GetValue()))
        except:
            raise ValueError(_("Invalid number for the via diameter."))

        if drill_diameter <= 0:
            raise ValueError(_("Too small drill diameter."))

        if drill_diameter > via_diameter:
            raise ValueError(
                _("The drill diameter is larger than the via diameter."))

        try:
            edge_distance = self._to_biu(
                Decimal(self.m_textCtrlEdgeDistance.GetValue()))
        except:
            raise ValueError(_("Invalid number for the edge distance."))

        if edge_distance <= 0:
            raise ValueError(_("The edge distance needs to be positive."))

        if not self.m_checkRandomize.GetValue():
            random_offset = 0
        else:
            try:
                random_offset = int(
                    Decimal(self.m_textCtrlRandomOffset.GetValue()))
            except:
                raise ValueError(_("Invalid number for the random offset."))

        if random_offset < 0 or random_offset > 100:
            raise ValueError(_("The random offset {" + str(random_offset) +
                               "} is outside the range [0 .. 100]."))

        try:
            solder_mask_margin = self._to_biu(
                Decimal(self.m_textCtrlSolderMaskMargin.GetValue()))
        except:
            raise ValueError(_("Invalid number for solder mask margin."))

        if solder_mask_margin < - via_diameter / 2:
            raise ValueError(_("Too small solder mask margin."))

        try:
            via_spacing = self._to_biu(
                Decimal(self.m_textCtrlViaSpacing.GetValue()))
        except:
            raise ValueError(_("Invalid number for via spacing."))

        if via_spacing < via_diameter:
            raise ValueError(
                _("The via spacing is smaller than the via diameter."))

        self.viastitching.is_staggered_rows = self.m_checkBoxStaggeredRows.GetValue()
        if self.m_checkBoxTentedVias.GetValue():
            self.viastitching.referenceVia.solder_mask_margin = 0
            # TODO disable the mask layer

        # Now assign zhe values
        self.viastitching.referenceVia.solder_mask_margin = solder_mask_margin
        self.viastitching.referenceVia.drill_diameter = drill_diameter
        self.viastitching.referenceVia.edge_distance = edge_distance
        self.viastitching.random_offset_factor = random_offset
        self.viastitching.referenceVia.via_diameter = via_diameter
        self.viastitching.via_spacing = via_spacing
        self.viastitching.random_offset_factor = random_offset
        self.viastitching.is_align_to_grid = self.m_checkAlignToGrid.GetValue()

        # Stitch now the vias
        self.m_staticTextProgress.Enable()
        self.m_staticTextProgressPercent.Enable()
        self.m_gaugeProgress.Enable()
        if self.m_checkStitchEdge.GetValue():
            self.viastitching.edge_distance = edge_distance
            # self.viastitching.stitch_edge_generator()
            for progress in self.viastitching.stitch_edge_generator():
                self.m_gaugeProgress.SetValue(int(progress))
                self.m_staticTextProgressPercent.SetLabel(str(progress) + "%")
        else:
            for progress in self.viastitching.stitch_zone_generator():
                self.m_gaugeProgress.SetValue(int(progress))
                self.m_staticTextProgressPercent.SetLabel(str(progress) + "%")

    def OnApplyButtonClick(self, event):
        '''
        This handler applies the via stitching to the board, if all user values are in valid ranges.
        :param event: is the event.
        '''
        try:
            self._checkValues()
            self.Destroy()
        except ValueError, e:
            dlg = wx.MessageDialog(self, _('Invalid values for via stitching!'), _(
                'Value error'), wx.OK | wx.ICON_ERROR)
            dlg.SetExtendedMessage(
                _("Please correct the following issue: ") + e.message)
            dlg.ShowModal()
        except RuntimeError, e:
            if e.message == "No zone was selected!":
                dlg = wx.MessageDialog(
                    self, _('No zone was selected!'), _('User error'), wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
        except:
            dlg = wx.MessageDialog(
                self, _('An error happened while trying to stitch the zone!'))

    def OnCancelButtonClick(self, event):
        '''
        Destroys the dialog window and does nothing else. 
        :param event: is the event.
        '''
        self.Destroy()


def start_dialog():
    dialog = ViaStitchingDialog(None)
    dialog.ShowModal()
