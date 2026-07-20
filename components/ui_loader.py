from pathlib import Path
import streamlit as st
from html import escape

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSS_DIR = PROJECT_ROOT / "assets" / "css"
HTML_DIR = PROJECT_ROOT / "assets" / "html"

def load_css(filename: str) -> None:
    css_path = CSS_DIR / filename

    if not css_path.exists():
        raise FileNotFoundError(
            f"CSSファイルが見つかりません: {css_path}"
        )
    
    css = css_path.read_text(encoding="utf-8")

    st.html(
        f"""
        <style>
        {css}
        </style>
        """
    )
    

from html import escape
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = PROJECT_ROOT / "assets" / "html"


def render_html(
    filename: str,
    variables: dict[str, object] | None = None
) -> None:
    html_path = HTML_DIR / filename

    #st.write("読込HTML:", html_path)
    #st.write("渡された変数:", variables)

    if not html_path.exists():
        raise FileNotFoundError(
            f"HTMLファイルが見つかりません: {html_path}"
        )

    html_text = html_path.read_text(encoding="utf-8")

    if variables:
        for name, value in variables.items():
            placeholder = f"{{{{{name}}}}}"

            html_text = html_text.replace(
                placeholder,
                escape(str(value))
            )

    #st.code(html_text)
    st.html(html_text)