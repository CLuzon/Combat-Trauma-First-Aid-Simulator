import streamlit as st
from components.ui_loader import load_css, render_html

def apply_field_manual_theme() -> None:
    """Apply the shared Field Manual visual theme to the current Streamlit page."""
    load_css("field_manual.css")


def manual_header(code: str, title: str, subtitle: str, section: str) -> None:
    render_html(
        "field_manual.html", {
            "code": code,
            "title": title,
            "subtitle": subtitle,
            "section": section
        }
    )