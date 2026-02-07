"""
Calculator Demo - Demonstrating zen-temple Architecture

This script demonstrates how the calculator example works in zen-temple:
1. Pure Python logic (CalculatorLogic) - Testable, reusable, framework-independent
2. Jinja template macro - Minimal bridge connecting logic to HTML
3. Flask server - Optional server to view the component in a browser
"""

import sys
from pathlib import Path

# Add parent directory to path to import calculator_logic
sys.path.insert(0, str(Path(__file__).parent))

from calculator_logic import CalculatorLogic


def demo_pure_logic():
    """Demonstrate the pure Python calculator logic."""
    print("=" * 60)
    print("1. Pure Python Logic Demo")
    print("=" * 60)
    
    calc = CalculatorLogic()
    
    # Example calculation: (5 + 3) * 2 = 16
    print("\nCalculation: (5 + 3) * 2")
    calc.input_digit("5")
    print(f"  Input 5: {calc.display}")
    
    calc.input_operation("+")
    print(f"  Operation +: {calc.display}")
    
    calc.input_digit("3")
    print(f"  Input 3: {calc.display}")
    
    calc.input_operation("*")  # This will calculate 5+3 first
    print(f"  Operation * (calculated): {calc.display}")
    
    calc.input_digit("2")
    print(f"  Input 2: {calc.display}")
    
    result = calc.calculate()
    print(f"  Final result: {result}")
    
    # Show history
    print(f"\nHistory:")
    for entry in calc.get_history():
        print(f"  {entry}")
    
    # Show context for templates
    print(f"\nTemplate context:")
    context = calc.to_context()
    for key, value in context.items():
        print(f"  {key}: {value}")


def demo_template_rendering():
    """Demonstrate rendering the calculator component with template."""
    print("\n" + "=" * 60)
    print("2. Template Rendering Demo")
    print("=" * 60)
    
    try:
        from zen_temple import TemplateManager
        
        # Set up template manager
        template_dir = Path(__file__).parent / "templates"
        manager = TemplateManager(template_dirs=[template_dir])
        
        print(f"\nTemplate directory: {template_dir}")
        print(f"Template exists: {template_dir.exists()}")
        
        # Render the index page with calculator
        if template_dir.exists():
            # The index.html uses components, so we just get the template directly
            template = manager.env.get_template("index.html")
            html = template.render()
            
            print(f"\nRendered HTML length: {len(html)} characters")
            print(f"Contains calculator macro: {'CalculatorState' in html}")
            print(f"Contains Alpine.js: {'x-data' in html}")
            
            # Save to output file for viewing
            output_file = Path(__file__).parent / "calculator_demo.html"
            output_file.write_text(html)
            print(f"\n✓ HTML saved to: {output_file}")
            print(f"  Open this file in a browser to see the calculator!")
        else:
            print("\n⚠ Template directory not found. Skipping render.")
            
    except Exception as e:
        print(f"\n⚠ Could not render template: {e}")


def demo_flask_server():
    """Provide instructions for running with Flask server."""
    print("\n" + "=" * 60)
    print("3. Flask Server Demo (Optional)")
    print("=" * 60)
    
    print("\nTo run the calculator with a Flask server:")
    print("  1. Install Flask: pip install flask")
    print("  2. Create app.py with the following code:")
    print()
    print("```python")
    print("from flask import Flask, render_template")
    print("from pathlib import Path")
    print()
    print("app = Flask(__name__,")
    print("            template_folder='examples/templates')")
    print()
    print("@app.route('/')")
    print("def index():")
    print("    return render_template('index.html')")
    print()
    print("if __name__ == '__main__':")
    print("    app.run(debug=True)")
    print("```")
    print()
    print("  3. Run: python app.py")
    print("  4. Open: http://localhost:5000")


def main():
    """Run all demos."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║       zen-temple Calculator Demo                         ║")
    print("║       Pure Logic + Minimal Bridge + Zero Legacy          ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    demo_pure_logic()
    demo_template_rendering()
    demo_flask_server()
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print("\nKey Principles Demonstrated:")
    print("  ✓ Logic is Pure: CalculatorLogic has no framework dependencies")
    print("  ✓ Bridge is Minimal: Jinja macro connects logic to template")
    print("  ✓ Zero Legacy: Clean separation enables easy testing & reuse")
    print()


if __name__ == "__main__":
    main()
