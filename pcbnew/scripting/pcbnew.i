/*
 * This program source code file is part of KiCad, a free EDA CAD application.
 *
 * Copyright (C) 2012 NBEE Embedded Systems, Miguel Angel Ajo <miguelangel@nbee.es>
 * Copyright (C) 1992-2012 KiCad Developers, see AUTHORS.txt for contributors.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, you may find one here:
 * http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
 * or you may search the http://www.gnu.org website for the version 2 license,
 * or you may write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
 */

/**
 * @file pcbnew.i
 * @brief Specific pcbnew wrappers
 */


%module pcbnew

%feature("autodoc", "1");
#ifdef ENABLE_DOCSTRINGS_FROM_DOXYGEN
%include "docstrings.i"
#endif

%include "kicad.i"

// ignore a couple of items that generate warnings from swig built code

%ignore BOARD_ITEM::ZeroOffset;
%ignore D_PAD::m_PadSketchModePenSize;
%ignore PCB_SCREEN::SetLastZoom;
%ignore PCB_SCREEN::SetPreviousZoom;
%ignore PCB_SCREEN::SetNextZoom();

// rename the Add method of classes to Add native, so we will handle
// the Add method in python

%rename(AddNative) *::Add;

// fix method names conflicts
%rename(AddChild) MODULE::Add;
%rename(RemoveChild) MODULE::Remove;
%rename(DeleteChild) MODULE::Delete;

typedef long long time_t; 

%exception {
    try{
        $action
    }
    catch( IO_ERROR e )
    {
        std::string str = TO_UTF8( e.errorText );
        str += '\n';
        PyErr_SetString( PyExc_IOError, str.c_str() );
        return NULL;
    }
    catch( std::exception &e )
    {
        std::string str = e.what();
        str += '\n';
        PyErr_SetString( PyExc_IOError, str.c_str() );
        return NULL;
    }
    catch( ... )
    {
        SWIG_fail;
    }
}
%include exception.i

%include <boost_shared_ptr.i>
%shared_ptr(NETCLASS)

// this is what it must be included in the wrapper .cxx code to compile

%{
  #include <wx_python_helpers.h>
  #include <class_board_item.h>
  #include <class_board_connected_item.h>
  #include <class_board_design_settings.h>
  #include <class_board.h>
  #include <class_module.h>
  #include <class_track.h>
  #include <class_zone.h>
  #include <zones.h>
  #include <layers_id_colors_and_visibility.h>
  #include <class_pad.h>
  #include <pad_shapes.h>
  #include <class_netinfo.h>
  #include <class_pcb_text.h>
  #include <class_dimension.h>
  #include <class_drawsegment.h>
  #include <class_marker_pcb.h>
  #include <class_mire.h>
  #include <class_text_mod.h>
  #include <class_edge_mod.h>
  #include <dlist.h>
  #include <class_zone_settings.h>
  #include <class_netclass.h>
  #include <class_netinfo.h>
  #include <class_pcb_screen.h>
  #include <zones.h>
  
  #include <boost/polygon/polygon.hpp>
  #include <../polygon/polygons_defs.h>

  #include <pcbnew_scripting_helpers.h>

  #include <plotcontroller.h>
  #include <pcb_plot_params.h>
  #include <exporters/gendrill_Excellon_writer.h>
  #include <colors.h>

  BOARD *GetBoard(); /* get current editor board */
  void RedrawGalCanvas(); /* Redraws the board */
  PCB_SCREEN* GetPcbScreen(); /* Get the current PCB screen */ 
  wxPoint GetGridSize(PCB_SCREEN* aPcbScreen); /* returns the grid size of the given screen */

  void SaveCopyInUndoList(const PICKED_ITEMS_LIST& aItemsList,
                            UNDO_REDO_T        aTypeCommand,
                            const wxPoint&     aTransformPoint);
  void OnModify();
%}

%{
  #include <io_mgr.h>
  #include <kicad_plugin.h>
%}

%include <class_board_item.h>
%include <class_board_connected_item.h>
%include <class_board_design_settings.h>
%include <class_board.h>
%include <class_module.h>
%include <class_track.h>
%include <class_zone.h>
%include <zones.h>
%include <layers_id_colors_and_visibility.h>
%include <class_pad.h>
%include <pad_shapes.h>
%include <class_netinfo.h>
%include <class_pcb_text.h>
%include <class_dimension.h>
%include <class_drawsegment.h>
%include <class_marker_pcb.h>
%include <class_mire.h>
%include <class_text_mod.h>
%include <class_edge_mod.h>
%include <dlist.h>
%include <class_zone_settings.h>
%include <class_netclass.h>
%include <class_netinfo.h>
%include <class_pcb_screen.h>
%include <zones.h>

%include <plotcontroller.h>
%include <pcb_plot_params.h>
%include <plot_common.h>
%include <exporters/gendrill_Excellon_writer.h>
%include <colors.h>

%include "board_item.i"

%include <pcbnew_scripting_helpers.h>

// Instantiate templates for pad vectors
%include "std_vector.i"
%template(PadVector) std::vector<D_PAD*>;

// ignore RELEASER as nested classes are still unsupported by swig
%ignore IO_MGR::RELEASER;
%include <io_mgr.h>
%include <kicad_plugin.h>

%include "board.i"
%include "module.i"
%include "plugins.i"
%include "units.i"

%include "tool.i"
%include "pnsrouter.i"
%include "view.i"
%include "gal.i"
