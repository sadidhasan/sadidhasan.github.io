#!/usr/bin/env python3
"""
Personal Website Generator
Generates a static website from config.yaml
"""

import yaml
import os
import shutil
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def load_config(config_path='config.yaml'):
    """Load configuration from YAML file"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_template(template_dir, template_name):
    """Load template file using Jinja2 Environment"""
    env = Environment(loader=FileSystemLoader(template_dir))
    return env.get_template(template_name)


def generate_site(config, output_dir='docs'):
    """Generate the website from config and templates"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean up config - remove None and empty values
    if config.get('experience') is None:
        config['experience'] = []
    if config.get('education') is None:
        config['education'] = []
    if config.get('skills') is None:
        config['skills'] = []
    if config.get('projects') is None:
        config['projects'] = []
    if config.get('certifications') is None:
        config['certifications'] = []
    if config.get('awards') is None:
        config['awards'] = []
    if config.get('additional') is None:
        config['additional'] = []
    if config.get('publications') is None:
        config['publications'] = []
    if config.get('students') is None:
        config['students'] = []
    if config.get('talks') is None:
        config['talks'] = []
    if config.get('news') is None:
        config['news'] = []
    
    # Preprocess bio text to handle newlines
    if 'personal' in config and 'bio' in config['personal']:
        config['personal']['bio'] = config['personal']['bio'].replace('\n', '<br>')
    
    # Preprocess additional sections
    if config.get('additional'):
        for section in config['additional']:
            if 'content' in section:
                section['content'] = section['content'].replace('\n', '<br>')
    
    # Group publications by year
    if config.get('publications'):
        from collections import OrderedDict
        pubs_by_year = OrderedDict()
        for pub in config['publications']:
            year = pub.get('year', 0)
            if year not in pubs_by_year:
                pubs_by_year[year] = []
            pubs_by_year[year].append(pub)
        config['publications_by_year'] = list(pubs_by_year.items())
    
    # Group patents by year
    if config.get('patents'):
        patents_by_year = OrderedDict()
        for pat in config['patents']:
            year = pat.get('year', 0)
            if year not in patents_by_year:
                patents_by_year[year] = []
            patents_by_year[year].append(pat)
        config['patents_by_year'] = list(patents_by_year.items())
    
    # Load templates
    html_template = load_template('templates', 'index.html')
    
    # Generate HTML
    html_content = html_template.render(config=config)
    
    # Write HTML file
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Copy CSS
    shutil.copy('templates/styles.css', os.path.join(output_dir, 'styles.css'))
    
    # Copy any additional assets if they exist
    if config.get('personal', {}).get('photo'):
        photo_path = config['personal']['photo']
        if os.path.exists(photo_path):
            shutil.copy(photo_path, output_dir)
    
    print(f"✅ Website generated successfully in '{output_dir}/' folder!")
    print(f"📁 Open {output_dir}/index.html in your browser to preview")
    print(f"🚀 Ready to deploy to GitHub Pages!")


def main():
    """Main function"""
    print("🌐 Personal Website Generator")
    print("=" * 50)
    
    # Check for custom config file argument
    config_file = 'config.yaml'
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        print(f"📝 Using custom config file: {config_file}")
    
    # Check if config exists
    if not os.path.exists(config_file):
        print(f"❌ Error: {config_file} not found!")
        print("Please create a config file with your information.")
        return
    
    # Check if templates exist
    if not os.path.exists('templates/index.html'):
        print("❌ Error: templates/index.html not found!")
        return
    
    if not os.path.exists('templates/styles.css'):
        print("❌ Error: templates/styles.css not found!")
        return
    
    # Load config
    print("📖 Loading configuration...")
    config = load_config(config_file)
    
    # Generate site
    print("🔨 Generating website...")
    generate_site(config)
    
    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. Preview: Open docs/index.html in your browser")
    print(f"2. Update: Edit {config_file} and run this script again")
    print("3. Deploy: Push to GitHub and enable GitHub Pages")


if __name__ == '__main__':
    main()
