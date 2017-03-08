# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class ViaStitchingDialogBase
###########################################################################

class ViaStitchingDialogBase ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Via Stitching"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizerAll = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizerViaProperties = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Via properties") ), wx.VERTICAL )
		
		self.m_bitmapStitchVia = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"stitchvia.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerViaProperties.Add( self.m_bitmapStitchVia, 0, wx.ALL, 5 )
		
		bSizerViaDiameter = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextViaDiameter = wx.StaticText( self, wx.ID_ANY, _(u"(a) Via diameter"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextViaDiameter.Wrap( -1 )
		bSizerViaDiameter.Add( self.m_staticTextViaDiameter, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrlViaDiameter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlViaDiameter.SetToolTipString( _(u"This value specifies the diameter of the stitched vias.") )
		
		bSizerViaDiameter.Add( self.m_textCtrlViaDiameter, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizerViaProperties.Add( bSizerViaDiameter, 0, 0, 5 )
		
		bSizerDrillDiameter = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextDrillDiameter = wx.StaticText( self, wx.ID_ANY, _(u"(b) Drill diameter"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextDrillDiameter.Wrap( -1 )
		bSizerDrillDiameter.Add( self.m_staticTextDrillDiameter, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrlDrillDiameter = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlDrillDiameter.SetToolTipString( _(u"This value determines the drill diameter of a stitched via.") )
		
		bSizerDrillDiameter.Add( self.m_textCtrlDrillDiameter, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizerViaProperties.Add( bSizerDrillDiameter, 0, 0, 5 )
		
		self.m_checkBoxTentedVias = wx.CheckBox( self, wx.ID_ANY, _(u"Tented vias"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxTentedVias.SetToolTipString( _(u"The vias are getting tented if this box is checked.") )
		
		sbSizerViaProperties.Add( self.m_checkBoxTentedVias, 0, wx.ALL, 5 )
		
		bSizerSolderMaskClearance = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextSolderMaskMargin = wx.StaticText( self, wx.ID_ANY, _(u"(c) Solder mask margin"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextSolderMaskMargin.Wrap( -1 )
		bSizerSolderMaskClearance.Add( self.m_staticTextSolderMaskMargin, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrlSolderMaskMargin = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlSolderMaskMargin.SetToolTipString( _(u"Determines the margin of the solder mask, negative values are allowed up to via diameter/2 for partially covered vias.") )
		
		bSizerSolderMaskClearance.Add( self.m_textCtrlSolderMaskMargin, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizerViaProperties.Add( bSizerSolderMaskClearance, 0, 0, 5 )
		
		self.m_buttonGetNetclassValues = wx.Button( self, wx.ID_ANY, _(u"Get netclass values"), wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerViaProperties.Add( self.m_buttonGetNetclassValues, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizerAll.Add( sbSizerViaProperties, 1, wx.EXPAND, 5 )
		
		bSizerStichingProperties = wx.BoxSizer( wx.VERTICAL )
		
		sbSizerStitchingProperties = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Stitching properties") ), wx.VERTICAL )
		
		self.m_bitmapStitchDistance = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"stitchdistance.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStitchingProperties.Add( self.m_bitmapStitchDistance, 0, wx.ALL, 5 )
		
		bSizerViaSpacing = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextViaSpacing = wx.StaticText( self, wx.ID_ANY, _(u"(d) Via spacing"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextViaSpacing.Wrap( -1 )
		bSizerViaSpacing.Add( self.m_staticTextViaSpacing, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrlViaSpacing = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlViaSpacing.SetToolTipString( _(u"This value determines the average distance of the stitched vias.") )
		
		bSizerViaSpacing.Add( self.m_textCtrlViaSpacing, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizerStitchingProperties.Add( bSizerViaSpacing, 0, 0, 5 )
		
		bSizerStaggered = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBoxStaggeredRows = wx.CheckBox( self, wx.ID_ANY, _(u"Staggered rows"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxStaggeredRows.SetToolTipString( _(u"If this box is checked, every second row is shifted on the x-axis by via distance / 2.") )
		
		bSizerStaggered.Add( self.m_checkBoxStaggeredRows, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_checkAlignToGrid = wx.CheckBox( self, wx.ID_ANY, _(u"Align vias to grid"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkAlignToGrid.SetToolTipString( _(u"If checked, try to align the vias to the actual user grid.") )
		
		bSizerStaggered.Add( self.m_checkAlignToGrid, 0, wx.ALL, 5 )
		
		self.m_checkStitchEdge = wx.CheckBox( self, wx.ID_ANY, _(u"Stitch zode edges only"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkStitchEdge.SetToolTipString( _(u"If checked, stitch the zone edges only, else the full zone.") )
		
		bSizerStaggered.Add( self.m_checkStitchEdge, 0, wx.ALL, 5 )
		
		bSizerViaSpacing1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextEdgeDistance = wx.StaticText( self, wx.ID_ANY, _(u"(e) Edge distance"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextEdgeDistance.Wrap( -1 )
		bSizerViaSpacing1.Add( self.m_staticTextEdgeDistance, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrlEdgeDistance = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlEdgeDistance.SetToolTipString( _(u"This value determines the distance of the stitched vias from the zone edge.") )
		
		bSizerViaSpacing1.Add( self.m_textCtrlEdgeDistance, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizerStaggered.Add( bSizerViaSpacing1, 1, wx.EXPAND, 5 )
		
		self.m_checkRandomize = wx.CheckBox( self, wx.ID_ANY, _(u"Randomize"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkRandomize.SetToolTipString( _(u"Randomize the via position.") )
		
		bSizerStaggered.Add( self.m_checkRandomize, 0, wx.ALL, 5 )
		
		
		sbSizerStitchingProperties.Add( bSizerStaggered, 0, 0, 5 )
		
		bSizerRandomOffset = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_labelRandomOffset = wx.StaticText( self, wx.ID_ANY, _(u"Random offset:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_labelRandomOffset.Wrap( -1 )
		bSizerRandomOffset.Add( self.m_labelRandomOffset, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrlRandomOffset = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlRandomOffset.SetToolTipString( _(u"The relative random offset factor, 0 .. 100 percent of the via spacing.") )
		
		bSizerRandomOffset.Add( self.m_textCtrlRandomOffset, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticUnit = wx.StaticText( self, wx.ID_ANY, _(u"%"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticUnit.Wrap( -1 )
		bSizerRandomOffset.Add( self.m_staticUnit, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizerStitchingProperties.Add( bSizerRandomOffset, 0, 0, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextProgress = wx.StaticText( self, wx.ID_ANY, _(u"Progress:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextProgress.Wrap( -1 )
		self.m_staticTextProgress.Enable( False )
		
		bSizer12.Add( self.m_staticTextProgress, 0, wx.ALL, 5 )
		
		self.m_gaugeProgress = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gaugeProgress.SetValue( 0 ) 
		self.m_gaugeProgress.Enable( False )
		
		bSizer12.Add( self.m_gaugeProgress, 0, wx.ALL, 5 )
		
		self.m_staticTextProgressPercent = wx.StaticText( self, wx.ID_ANY, _(u"0%"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextProgressPercent.Wrap( -1 )
		self.m_staticTextProgressPercent.Enable( False )
		
		bSizer12.Add( self.m_staticTextProgressPercent, 0, wx.ALL, 5 )
		
		
		sbSizerStitchingProperties.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		
		bSizerStichingProperties.Add( sbSizerStitchingProperties, 1, wx.EXPAND, 5 )
		
		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1Apply = wx.Button( self, wx.ID_APPLY )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Apply )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		
		bSizerStichingProperties.Add( m_sdbSizer1, 0, wx.ALIGN_RIGHT, 5 )
		
		
		bSizerAll.Add( bSizerStichingProperties, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizerAll )
		self.Layout()
		bSizerAll.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_checkBoxTentedVias.Bind( wx.EVT_CHECKBOX, self.OnTentedViasCheckBox )
		self.m_buttonGetNetclassValues.Bind( wx.EVT_BUTTON, self.OnGetNetclassValuesButtonClick )
		self.m_checkBoxStaggeredRows.Bind( wx.EVT_CHECKBOX, self.OnStaggeredRowsCheckBox )
		self.m_checkAlignToGrid.Bind( wx.EVT_CHECKBOX, self.OnStaggeredRowsCheckBox )
		self.m_checkStitchEdge.Bind( wx.EVT_CHECKBOX, self.OnStitchEdgesCheckBox )
		self.m_checkRandomize.Bind( wx.EVT_CHECKBOX, self.OnRandomizeCheckBox )
		self.m_sdbSizer1Apply.Bind( wx.EVT_BUTTON, self.OnApplyButtonClick )
		self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.OnCancelButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnTentedViasCheckBox( self, event ):
		event.Skip()
	
	def OnGetNetclassValuesButtonClick( self, event ):
		event.Skip()
	
	def OnStaggeredRowsCheckBox( self, event ):
		event.Skip()
	
	
	def OnStitchEdgesCheckBox( self, event ):
		event.Skip()
	
	def OnRandomizeCheckBox( self, event ):
		event.Skip()
	
	def OnApplyButtonClick( self, event ):
		event.Skip()
	
	def OnCancelButtonClick( self, event ):
		event.Skip()
	

