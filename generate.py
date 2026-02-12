#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


BASE_DIR = Path(__file__).parent


def load_yaml(path: Path) -> dict:
    """Load YAML file."""
    with open(path) as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def load_config() -> dict:
    """Load config.yaml."""
    return load_yaml(BASE_DIR / 'config.yaml')


def render_template(data: dict, template_path: Path) -> str:
    """Render Jinja2 template with CV data."""
    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<#',
        comment_end_string='#>',
    )
    template = env.get_template(template_path.name)
    return template.render(data)


def compile_pdf(tex_path: Path, output_path: Path) -> bool:
    """Compile LaTeX file to PDF using pdflatex."""
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', f'-output-directory={output_dir}', tex_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"pdflatex error:\n{result.stdout}", file=sys.stderr)
            return False

        # Rename PDF to desired output name
        generated_pdf = output_dir / tex_path.with_suffix('.pdf').name
        if generated_pdf != output_path:
            generated_pdf.rename(output_path)

        return True
    except FileNotFoundError:
        print("Error: pdflatex not found. Please install a LaTeX distribution.", file=sys.stderr)
        return False


def cleanup_aux_files(output_dir: Path, stem: str):
    """Remove intermediate LaTeX files."""
    extensions = ['.aux', '.log', '.out', '.fls', '.fdb_latexmk', '.synctex.gz', '.tex']
    for ext in extensions:
        aux_file = output_dir / f"{stem}{ext}"
        if aux_file.exists():
            aux_file.unlink()


def generate_cv(name: str, cv_config: dict, defaults: dict) -> bool:
    """Generate a single CV."""
    data_path = BASE_DIR / cv_config['data']
    template_path = BASE_DIR / cv_config.get('template', defaults.get('template'))
    output_path = BASE_DIR / cv_config['output']

    print(f"Generating {name}...")

    # Load data and render template
    data = load_yaml(data_path)
    output = render_template(data, template_path)

    # Write .tex file to output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tex_path = output_path.with_suffix('.tex')
    with open(tex_path, 'w') as f:
        f.write(output)

    # Compile to PDF
    if not compile_pdf(tex_path, output_path):
        print(f"Failed to generate {name}", file=sys.stderr)
        return False

    # Clean up intermediate files
    cleanup_aux_files(output_path.parent, tex_path.stem)

    print(f"  -> {output_path}")
    return True


def list_cvs(config: dict):
    """List available CV configurations."""
    print("Available CVs:")
    for name, cv_config in config.get('cvs', {}).items():
        print(f"  {name}")
        print(f"    data: {cv_config['data']}")
        print(f"    template: {cv_config.get('template', config.get('defaults', {}).get('template'))}")
        print(f"    output: {cv_config['output']}")


def main():
    parser = argparse.ArgumentParser(description='Generate CV PDFs')
    parser.add_argument('cv_name', nargs='?', help='Name of CV to generate (generates all if not specified)')
    parser.add_argument('--list', '-l', action='store_true', help='List available CVs')
    args = parser.parse_args()

    config = load_config()
    defaults = config.get('defaults', {})
    cvs = config.get('cvs', {})

    if args.list:
        list_cvs(config)
        return

    if args.cv_name:
        if args.cv_name not in cvs:
            print(f"Error: CV '{args.cv_name}' not found in config.yaml", file=sys.stderr)
            print("Available CVs:", ', '.join(cvs.keys()), file=sys.stderr)
            sys.exit(1)
        success = generate_cv(args.cv_name, cvs[args.cv_name], defaults)
        if not success:
            sys.exit(1)
    else:
        # Generate all CVs
        failed = []
        for name, cv_config in cvs.items():
            if not generate_cv(name, cv_config, defaults):
                failed.append(name)

        if failed:
            print(f"\nFailed to generate: {', '.join(failed)}", file=sys.stderr)
            sys.exit(1)

        print(f"\nSuccessfully generated {len(cvs)} CV(s)")


if __name__ == '__main__':
    main()
