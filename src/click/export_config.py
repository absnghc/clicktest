#"This is a test file"

"""
Export configuration endpoint.

This module provides functionality to export Click application configuration
to multiple formats (JSON, YAML, etc).
"""

import json
import click
from datetime import datetime
from typing import Dict, Any, Optional


def build_config_dict(ctx: click.Context) -> Dict[str, Any]:
    """
    Build configuration dictionary from context.
    
    Args:
        ctx: Click context object
        
    Returns:
        Dictionary containing application configuration
    """
    config = {
        'version': getattr(ctx, 'version', '1.0.0'),
        'timestamp': datetime.now().isoformat(),
        'settings': {
            'debug': ctx.obj.get('debug', False) if ctx.obj else False,
            'verbose': ctx.obj.get('verbose', False) if ctx.obj else False,
        },
        'info': {
            'command': ctx.info_name,
            'parent': ctx.parent.info_name if ctx.parent else None,
        }
    }
    return config


@click.command('export-config')
@click.option('--format', 
              type=click.Choice(['json', 'text']), 
              default='json',
              help='Export format')
@click.option('--output', 
              type=click.File('w'), 
              default='-',
              help='Output file (default: stdout)')
@click.option('--indent', 
              type=int, 
              default=2,
              help='JSON indentation level')
@click.pass_context
def export_config_command(ctx, format, output, indent):
    """
    Export current application configuration.
    
    This command exports the current Click application's configuration
    including settings, context information, and metadata.
    """
    try:
        config = build_config_dict(ctx)
        
        if format == 'json':
            json.dump(config, output, indent=indent)
            output.write('\n')
        else:  # text format
            for key, value in config.items():
                output.write(f'{key}: {value}\n')
        
        click.echo('✓ Configuration exported successfully', err=True)
        return 0
        
    except Exception as e:
        click.echo(f'✗ Error exporting configuration: {str(e)}', err=True)
        raise click.ClickException(f'Export failed: {str(e)}')


if __name__ == '__main__':
    export_config_command()
