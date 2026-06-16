// This will be loaded automatically by Dash since it's in the assets folder

// Function to add interactivity to the SVG
function addSvgInteractivity() {
    const svgElement = document.getElementById('philippines-map');
    if (!svgElement) {
        setTimeout(addSvgInteractivity, 500);
        return;
    }
    
    const regions = svgElement.querySelectorAll('path');
    
    regions.forEach(region => {
        const originalFill = region.getAttribute('fill');
        
        // Add hover effects
        region.addEventListener('mouseenter', () => {
            region.setAttribute('fill', '#4cc9f0');
            region.style.cursor = 'pointer';
        });
        
        region.addEventListener('mouseleave', () => {
            region.setAttribute('fill', originalFill);
        });
        
        // Add click handler
        region.addEventListener('click', () => {
            const regionId = region.getAttribute('id');
            
            // Dispatch an event that Dash can capture
            const event = new CustomEvent('regionClicked', {
                detail: { regionId: regionId }
            });
            document.dispatchEvent(event);
        });
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', addSvgInteractivity);