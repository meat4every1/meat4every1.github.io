// Function to load sidebar content
function loadSidebarContent() {
    console.log('loadSidebarContent function called');
    const sidebar = document.getElementById('sidebar');
    const topToggle = document.getElementById('topToggle');
    console.log('Sidebar element found:', sidebar);
    if (sidebar) {
        console.log('Sidebar display style:', sidebar.style.display);
        console.log('Sidebar computed display:', window.getComputedStyle(sidebar).display);
    }
    console.log('Top toggle element found:', topToggle);
    if (topToggle) {
        console.log('Top toggle display style:', topToggle.style.display);
        console.log('Top toggle computed display:', window.getComputedStyle(topToggle).display);
    }
    
    if (sidebar || topToggle) {
        // Add timestamp to prevent caching
        const timestamp = new Date().getTime();
        fetch(`sidebar-content.html?t=${timestamp}`)
            .then(response => {
                console.log('Fetch response status:', response.status);
                return response.text();
            })
            .then(data => {
                console.log('Sidebar content loaded, length:', data.length);
                console.log('First 200 characters:', data.substring(0, 200));
                
                // Load content into sidebar if it exists
                if (sidebar) {
                    sidebar.innerHTML = data;
                }
                
                // Load content into top toggle if it exists
                if (topToggle) {
                    // For top toggle, we only want the social media section
                    // Create a temporary div to parse the HTML
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = data;
                    
                    // Find the social media article
                    const socialArticle = tempDiv.querySelector('.social');
                    if (socialArticle) {
                        // Replace the existing social content in top toggle
                        const existingSocial = topToggle.querySelector('.social');
                        if (existingSocial) {
                            existingSocial.innerHTML = socialArticle.innerHTML;
                        } else {
                            // If no existing social div, create one
                            const newSocialDiv = document.createElement('div');
                            newSocialDiv.className = 'social';
                            newSocialDiv.style.paddingLeft = '3%';
                            newSocialDiv.innerHTML = socialArticle.innerHTML;
                            
                            // Find the staticBlock and replace its content
                            const staticBlock = topToggle.querySelector('.staticBlock');
                            if (staticBlock) {
                                staticBlock.innerHTML = '';
                                staticBlock.appendChild(newSocialDiv);
                            }
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error loading sidebar content:', error);
                // Fallback content if loading fails
                const fallbackContent = `
                    <article>
                        <div class="social" style="display: inline;">
                            <ul>
                                <li><img src="Img/SMB_M.jpg"></li>
                                <li><img src="Img/SMB_4.jpg"></li>
                                <li><img src="Img/SMB_E.jpg"></li>
                                <li><img src="Img/SMB_1.jpg"></li>
                                <li><a href="https://twitter.com/Meat4every1"><img src="Img/SMB_twitter.jpg"></a></li>
                                <li><a href="https://www.linkedin.com/in/ian-woskey-059a997b"><img src="Img/SMB_linkedin.jpg"></a></li>
                                <li><a href="https://www.facebook.com/meat4every1/"><img src="Img/SMB_facebook.jpg"></a></li>
                                <li><a href="https://www.instagram.com/meat4every1/"><img src="Img/SMB_instagram.jpg"></a></li>
                            </ul>
                        </div>
                    </article>
                    <article style="padding-bottom:1%;">
                        <iframe id="chunker" src="http://streambadge.com/twitch/dark/meat4every1/" style="height: 64px;"></iframe>
                        <a href="https://www.twitch.tv/meat4every1">
                            <div id="follow">
                                <p>Follow me on Twitch!</p>
                            </div>
                        </a>
                    </article>
                    <article>
                        <div>
                            <h2>Ian C. Woskey</h2>
                            <p>iancwoskey@gmail.com</p>
                            <p>Digital Media Bs/Ms</p>
                            <p>Drexel University</p>
                            <a href="text/Resume.pdf">Resume Pdf</a>
                        </div>
                    </article>
                `;
                
                if (sidebar) {
                    sidebar.innerHTML = fallbackContent;
                }
                
                if (topToggle) {
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = fallbackContent;
                    const socialArticle = tempDiv.querySelector('.social');
                    if (socialArticle) {
                        const existingSocial = topToggle.querySelector('.social');
                        if (existingSocial) {
                            existingSocial.innerHTML = socialArticle.innerHTML;
                        }
                    }
                }
            });
    }
}

// Load sidebar content when the page is ready
document.addEventListener('DOMContentLoaded', loadSidebarContent);

// Also try loading after a short delay to ensure layout functions have run
setTimeout(loadSidebarContent, 100);

// Try loading after layoutShift function has run
setTimeout(loadSidebarContent, 500);

// Also try loading when window loads completely
window.addEventListener('load', loadSidebarContent); 