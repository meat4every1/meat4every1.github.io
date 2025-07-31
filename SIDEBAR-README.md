# Dynamic Sidebar System

## Overview
Your website now uses a dynamic sidebar and top toggle system that loads content from a single file. This means you only need to edit one file to update both the sidebar (desktop) and top toggle (mobile) across all pages.

## How It Works

### Files Created:
1. **`sidebar-content.html`** - Contains all the sidebar content
2. **`sidebar-loader.js`** - JavaScript that loads the sidebar content dynamically
3. **`SIDEBAR-README.md`** - This documentation file

### How to Update the Sidebar and Top Toggle:
1. Open `sidebar-content.html`
2. Edit the content as needed
3. Save the file
4. The changes will appear on all pages automatically (both desktop sidebar and mobile top toggle)

### What Was Changed:
- All HTML files now have a simple `<aside id="sidebar">` container
- The `topToggle` section now loads content dynamically instead of being hardcoded
- The `sidebar-loader.js` script is included in each page
- The script automatically loads content from `sidebar-content.html` into both sidebar and top toggle

## Benefits:
- ✅ **Single source of truth** - Edit one file, update all pages
- ✅ **Consistent content** - Both desktop sidebar and mobile top toggle show the same content
- ✅ **Easy maintenance** - No more editing multiple files
- ✅ **Fallback support** - If loading fails, shows default content

## Technical Details:
- Uses JavaScript `fetch()` to load content
- Includes error handling with fallback content
- Works with your existing responsive design
- Compatible with all modern browsers

## Files That Need Manual Updates:
If you add new HTML pages, you need to:
1. Add `<script src="sidebar-loader.js"></script>` in the head section
2. Add `<aside id="sidebar"></aside>` where you want the sidebar

## Troubleshooting:
- If the sidebar doesn't load, check that `sidebar-loader.js` is included
- Make sure `sidebar-content.html` exists in the same directory
- Check browser console for any JavaScript errors 