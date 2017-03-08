/*
 * This program source code file is part of KiCad, a free EDA CAD application.
 *
 * Copyright (C) 2015 Torsten Hueter <torstenhtr@gmx.de>
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
 * @file tool.i
 * @brief Wrappers for the tool framework.
 */

%{
  #include <../include/tool/tool_base.h>
  #include <../include/tool/tool_interactive.h>
  #include <../include/tool/tool_manager.h>
  
  #include <tools/selection_tool.h>
  #include <tools/edit_points.h>
  #include <tools/point_editor.h>
  
  #include <pcbnew_scripting_helpers.h>
  TOOL_MANAGER* GetToolManager(); ///< Get the tool manager of the current editor frame
%}

%include <../include/tool/tool_base.h>
%include <../include/tool/tool_interactive.h>
%include <../include/tool/tool_manager.h>

%include <tools/selection_tool.h>
%include <tools/edit_points.h>
%include <tools/point_editor.h>

%inline
{
    SELECTION_TOOL* Cast_to_SELECTION_TOOL(TOOL_BASE* tool_base)
    {
        return dynamic_cast<SELECTION_TOOL*>(tool_base);
    }
    POINT_EDITOR* Cast_to_POINT_EDITOR(TOOL_BASE* tool_base)
    {
        return dynamic_cast<POINT_EDITOR*>(tool_base);
    }
}
