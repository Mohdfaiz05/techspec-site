// Centralized Affiliate Configuration for TechSpec India
// Change the Amazon Associate tag here to update all buy links across the entire site instantly.
const AMAZON_TAG = "techspecin05-21";

// Dynamic helper: automatically appends or updates the tracking tag on any Amazon link clicked
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('a[href*="amazon.in"]').forEach((link) => {
    try {
      const url = new URL(link.href);
      if (url.hostname.includes("amazon.in")) {
        url.searchParams.set("tag", AMAZON_TAG);
        link.href = url.toString();
        link.setAttribute("rel", "nofollow sponsored noopener");
        link.setAttribute("target", "_blank");
      }
    } catch (e) {
      // Ignore relative or invalid URLs
    }
  });
});
