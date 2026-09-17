#!/bin/bash
# Force the Dock and Finder to pick up a newly-changed app icon.
#
# killall Dock alone is NOT enough: IconServices caches the rendered icon per
# app, keyed off the bundle's mtime, and the Dock reads from that cache. Without
# clearing it the old icon survives a Dock restart, which is why the icon only
# updates after removing the app from the Dock and re-adding it.
#
# Usage: refresh_dock.sh /Applications/Foo.app [/Applications/Bar.app ...]
# No sudo needed; only the per-user cache is touched.

set -u
LSREGISTER=/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister

for app in "$@"; do
    [ -e "$app" ] || { echo "skip (not found): $app"; continue; }
    note=""
    # Bump mtime so the cache key changes. Root-owned bundles (Outlook, some
    # installers) refuse this without sudo; the cache purge below usually still
    # does the job, so carry on rather than bailing out.
    touch "$app" 2>/dev/null || note=" (mtime bump denied - root-owned)"
    "$LSREGISTER" -f "$app" 2>/dev/null # re-register with LaunchServices
    echo "refreshed: $app$note"
done

# Drop the per-user rendered-icon caches, then let the agents rebuild them.
killall iconservicesagent iconservicesd 2>/dev/null
rm -rf "$(getconf DARWIN_USER_CACHE_DIR)"com.apple.iconservices* 2>/dev/null
rm -rf "$TMPDIR"com.apple.iconservices* 2>/dev/null

killall Dock 2>/dev/null
killall Finder 2>/dev/null
echo "Dock and Finder restarted."
