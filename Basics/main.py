from kivy.app import App
from kivy.uix.widget import Widget
# from kivy.uix.button import Button


class CustomWidget(Widget):
	pass


class CustomWidgetApp(App):
	def build(self):
		return CustomWidget()


test = CustomWidgetApp()
test.run()
