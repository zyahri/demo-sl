/**
 * GLOBAL FOOTER COMPONENT - DEMO SLOT THEME
 * ------------------------------------------------
 * Centralized footer that is automatically injected into all pages.
 */

const GLOBAL_FOOTER_CONTENT = `
<footer class="sk-footer">
    <div class="sk-footer-top">
        <div class="sk-top-left">
            <h2>Play Thousands of Free<br>Anti-Lag Demo Slots</h2>
        </div>
        
        <div class="sk-top-right">
            <div class="sk-app-icon">RTP</div>
            
            <div class="style-text">
                <div style="font-weight:700; font-size:0.9rem;">Winning Pattern Updates</div>
                <div style="font-size:0.75rem; color:#ccc; display: flex; align-items: center; gap: 5px; margin-top: 3px;">
                    98.5% 
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="#facc15">
                        <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
                    </svg> 
                    <span style="color:#666">• High Winrate</span>
                </div>
            </div>
            
            <div class="sk-dl-group">
               <button style="background:transparent; border:1px solid #333; color:white; padding:8px 15px; border-radius:5px; cursor:pointer; font-size:0.8rem;">Android APK</button>
            </div>
        </div>
    </div>

    <div class="sk-footer-links">
        <div class="sk-col">
            <h4>POPULAR PROVIDERS</h4>
            <a href="#" class="sk-li">Pragmatic Play</a>
            <a href="#" class="sk-li">PG Soft</a>
            <a href="#" class="sk-li">Habanero</a>
            <a href="#" class="sk-li">Spadegaming</a>
            <a href="#" class="sk-li">Microgaming</a>
            <a href="#" class="sk-li">NoLimit City</a>
        </div>
        
        <div class="sk-col">
            <h4>HOT GAMES TODAY</h4>
            <a href="#" class="sk-li">Gates of Olympus</a>
            <a href="#" class="sk-li">Starlight Princess</a>
            <a href="#" class="sk-li">Mahjong Ways 2</a>
            <a href="#" class="sk-li">Sweet Bonanza</a>
            <a href="#" class="sk-li">Sugar Rush 1000</a>
            <a href="#" class="sk-li">Wild Bandito</a>
        </div>
        
        <div class="sk-col">
            <h4>INFORMATION</h4>
            <a href="#" class="sk-li">About Us</a>
            <a href="#" class="sk-li">Contact Us</a>
            <a href="#" class="sk-li">Privacy Policy</a>
            <a href="#" class="sk-li">Terms of Service</a>
            <a href="#" class="sk-li">Disclaimer</a>
        </div>
        
        <div class="sk-col">
            <h4>PARTNERS & PBN</h4>
            <a href="#" class="sk-li" target="_blank">Gacor Slot Site 1</a>
            <a href="#" class="sk-li" target="_blank">Gacor Slot Site 2</a>
            <a href="#" class="sk-li" target="_blank">Updated Live RTP</a>
            <a href="#" class="sk-li" target="_blank">ID Slot Community</a>
        </div>
    </div>

    <div class="sk-brand-row"></div>

    <div class="sk-bottom-info">
        <div class="sk-office-box">
            <div class="sk-office-title">THE DATABASE</div>
            <p>This site provides free demo slot accounts for entertainment purposes only. No real money is used in these demo games.</p>
        </div>
        <div class="sk-about-box">
            <div class="sk-office-title">COPYRIGHT</div>
            <p>&copy; 2024 Professional Demo. All rights reserved. Game assets are property of their respective providers.</p>
        </div>
    </div>
</footer>`;

/**
 * AUTO-INJECTION LOGIC
 * Injects the footer HTML into the div with id "global-footer-placeholder"
 */
document.addEventListener("DOMContentLoaded", function() {
    const placeholder = document.getElementById("global-footer-placeholder");
    if (placeholder) {
        placeholder.innerHTML = GLOBAL_FOOTER_CONTENT;
    }
});