from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label

# TODO: এখানে আপনার হোস্ট করা ওয়েবসাইটের লিংক বসান (https দিয়ে)
SITE_URL = "https://YOUR-APP-URL.onrender.com"

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
    activity = PythonActivity.mActivity
    webview = WebView(activity)
    settings = webview.getSettings()
    settings.setJavaScriptEnabled(True)
    settings.setDomStorageEnabled(True)
    webview.setWebViewClient(WebViewClient())
    activity.setContentView(webview)
    webview.loadUrl(SITE_URL)


@run_on_ui_thread
def go_back():
    if webview is not None and webview.canGoBack():
        webview.goBack()


class MainApp(App):
    def build(self):
        Window.bind(on_keyboard=self.on_key)
        if ON_ANDROID:
            create_webview()
        return Label(text="Loading...")

    def on_key(self, window, key, *args):
        # Back button
        if key == 27 and ON_ANDROID and webview is not None:
            go_back()
            return True
        return False


if __name__ == "__main__":
    MainApp().run()
