#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


def load_data(yaml_path: str) -> dict:
    """Load CV data from YAML file."""
    with open(yaml_path) as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def render_template(data: dict, template_dir: str, template_name: str) -> str:
    """Render Jinja2 template with CV data."""
    env = Environment(
        loader=FileSystemLoader(template_dir),
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<#',
        comment_end_string='#>',
    )
    template = env.get_template(template_name)
    return template.render(data)


def compile_pdf(tex_path: Path) -> bool:
    """Compile LaTeX file to PDF using pdflatex."""
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', tex_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"pdflatex error:\n{result.stdout}", file=sys.stderr)
            return False
        return True
    except FileNotFoundError:
        print("Error: pdflatex not found. Please install a LaTeX distribution.", file=sys.stderr)
        return False


def cleanup_aux_files(base_path: Path):
    """Remove intermediate LaTeX files."""
    extensions = ['.aux', '.log', '.out', '.fls', '.fdb_latexmk', '.synctex.gz']
    for ext in extensions:
        aux_file = base_path.with_suffix(ext)
        if aux_file.exists():
            aux_file.unlink()


def main():
    base_dir = Path(__file__).parent
    yaml_path = base_dir / 'my_data.yaml'
    tex_path = base_dir / 'cv.tex'

    # Load data and render template
    data = load_data(yaml_path)
    output = render_template(data, base_dir, 'cv.tex.jinja')

    # Write .tex file
    with open(tex_path, 'w') as f:
        f.write(output)
    print(f"Generated {tex_path}")

    # Compile to PDF
    print("Compiling PDF...")
    if compile_pdf(tex_path):
        print(f"Successfully generated {base_dir / 'cv.pdf'}")
    else:
        print("PDF compilation failed", file=sys.stderr)
        sys.exit(1)

    # Clean up intermediate files
    cleanup_aux_files(tex_path)


if __name__ == '__main__':
    main()
