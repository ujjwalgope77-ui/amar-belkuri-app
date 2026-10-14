from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

SITE_URL = "https://amar-belkuri-app.onrender.com/"

webview = None

try:
    from android.runnable import run_on_ui_thread
    from jnius import autoclass

    WebView = autoclass("android.webkit.WebView")
    WebViewClient = autoclass("android.webkit.WebViewClient")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    ON_ANDROID = True
except ImportError:
    ON_ANDROID = False

    def run_on_ui_thread(f):
        return f


@run_on_ui_thread
def create_webview():
    global webview
    try:
        activity = PythonActivity.mActivity
        webview = WebView(activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setLoadWithOverviewMode(True)
        settings.setUseWideViewPort(True)
        webview.setWebViewClient(WebViewClient())
        activity.setContentView(webview)
        webview.requestFocus()
        webview.loadUrl(SITE_URL)
    except Exception as e:
        print("WEBVIEW ERROR:", e)


@run_on_ui_thread
def go_back():
    if webview is not None and webview.canGoBack():
        webview.goBack()
    else:
        PythonActivity.mActivity.finish()


class MainApp(App):
    def build(self):
        Window.bind(on_keyboard=self.on_key)
        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)
        layout.add_widget(Image(source="ab.png"))
        layout.add_widget(Label(
            text="Loading... (first load may take up to 1 minute)",
            size_hint_y=0.2,
        ))
        return layout

    def on_start(self):
        if ON_ANDROID:
            create_webview()

    def on_key(self, window, key, *args):
        if key == 27 and ON_ANDROID:
            go_back()
            return True
        return False


if __name__ == "__main__":
    MainApp().run()
