"""
Prompt template manager for loading and rendering prompt templates from text files.
"""

import os
from pathlib import Path
from typing import List, Dict
import string


class PromptManager:
    """Manages prompt templates stored as text files."""
    
    def __init__(self, templates_dir: str = 'prompt_templates'):
        """
        Initialize the prompt manager.
        
        Args:
            templates_dir: Directory where prompt templates are stored
        """
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(exist_ok=True)
    
    def list_templates(self) -> List[str]:
        """
        Get list of available templates.
        
        Returns:
            List of template filenames (.txt files)
        """
        if not self.templates_dir.exists():
            return []
        
        templates = [
            f.name for f in self.templates_dir.glob('*.txt')
        ]
        return sorted(templates)
    
    def get_template(self, template_name: str) -> str:
        """
        Load a template from a text file.
        
        Args:
            template_name: Name of the template file (e.g., 'my_template.txt')
        
        Returns:
            Content of the template file
        
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f'Template not found: {template_name}')
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def save_template(self, template_name: str, content: str) -> None:
        """
        Save a template to a text file.
        
        Args:
            template_name: Name of the template file
            content: Content to save
        """
        template_path = self.templates_dir / template_name
        self.templates_dir.mkdir(exist_ok=True)
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def render_template(self, template: str, **kwargs) -> str:
        """
        Render a template by replacing placeholders with provided values.
        
        Supports simple placeholder syntax: {variable_name}
        
        Args:
            template: Template content with placeholders
            **kwargs: Variables to substitute in the template
        
        Returns:
            Rendered template with placeholders replaced
        
        Example:
            template = "Answer this question: {question}"
            rendered = manager.render_template(template, question="What is Python?")
            # Result: "Answer this question: What is Python?"
        """
        try:
            return string.Formatter().vformat(template, (), kwargs)
        except KeyError as e:
            raise ValueError(f'Missing template variable: {e}')
    
    def delete_template(self, template_name: str) -> None:
        """
        Delete a template file.
        
        Args:
            template_name: Name of the template file
        
        Raises:
            FileNotFoundError: If template doesn't exist
        """
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f'Template not found: {template_name}')
        
        template_path.unlink()
