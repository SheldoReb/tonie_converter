from jinja2 import Environment, FileSystemLoader
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

# Beispiel: Übersicht

def render_overview(sessions, tracks):
    template = env.get_template('overview.html')
    return template.render(sessions=sessions, tracks=tracks)
