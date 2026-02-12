# my-cv

Generate professional PDF CVs from YAML data using Jinja2 templates and LaTeX.

## Requirements

- Python 3.x
- LaTeX distribution with `pdflatex` (e.g., TeX Live, MacTeX)
- Python packages: `jinja2`, `pyyaml`

### Installation

```bash
# Install Python dependencies
pip install jinja2 pyyaml

# Install LaTeX (macOS)
brew install --cask mactex

# Install LaTeX (Ubuntu/Debian)
sudo apt-get install texlive-latex-extra texlive-fonts-extra
```

## Project Structure

```
my-cv/
├── config.yaml          # CV variant definitions
├── generate.py          # Generator script
├── data/                # YAML data files
│   └── java-engineer.yaml
├── templates/           # Jinja2 LaTeX templates
│   └── banking.tex.jinja
└── output/              # Generated PDFs (gitignored)
```

## Usage

```bash
# Generate all CVs defined in config.yaml
python generate.py

# Generate a specific CV
python generate.py java-engineer

# List available CVs
python generate.py --list
```

## Adding a New CV

1. Create a data file in `data/`:
   ```yaml
   # data/my-new-cv.yaml
   personal:
     firstName: John
     lastName: Doe
     jobTitle: Software Engineer
     # ...
   ```

2. Add an entry to `config.yaml`:
   ```yaml
   cvs:
     my-new-cv:
       data: data/my-new-cv.yaml
       template: templates/banking.tex.jinja
       output: output/my-new-cv.pdf
   ```

3. Generate:
   ```bash
   python generate.py my-new-cv
   ```

## Templates

Templates use [moderncv](https://ctan.org/pkg/moderncv) LaTeX class. Available styles:
- `banking` - Clean, corporate look (default)
- `classic` - Traditional CV layout
- `casual` - Relaxed with photo
- `oldstyle` - Vintage appearance
- `fancy` - Modern decorative

To create a new template style, copy `templates/banking.tex.jinja` and modify the `\moderncvstyle{...}` line.

## GitHub Actions

The workflow automatically generates all CVs on push to `release` branch. PDFs are available as downloadable artifacts in the Actions tab.

Manual trigger is also available via `workflow_dispatch`.

## License

Apache 2.0
