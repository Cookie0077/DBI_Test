from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("button_hinzufuegen", "click")
  def button_hinzufuegen_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('Query_Insert_Mitglied',self.item["mitglied_id"],self.item["kurs_id"])

    
