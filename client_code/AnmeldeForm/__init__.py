from ._anvil_designer import AnmeldeFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class AnmeldeForm(AnmeldeFormTemplate):
  def __init__(self,Kurs_dict, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

 
    self.kurs_id = Kurs_dict["kurs_id"] 
    Mitglieder = anvil.server.call("Query_Get_Mitglieder", self.kurs_id)
    self.repeating_panel_Mitglieder.items = Mitglieder

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Kursuebersicht')
