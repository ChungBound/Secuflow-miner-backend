#!/usr/bin/env python3
"""Test imports for deployment"""
try:
    from main import app
    print("✅ Import successful! App created:", type(app).__name__)
    print("🎉 Ready for deployment!")
except ImportError as e:
    print("❌ Import error:", e)
    sys.exit(1)
except Exception as e:
    print("❌ Error:", e)
    import traceback
    traceback.print_exc()
    sys.exit(1)
