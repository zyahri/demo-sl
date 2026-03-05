// --- FUNCTION TO CONVERT GAME NAME TO URL ---
function slugify(text) {
    if (!text) return 'unknown';
    return text.toString().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

// --- GLOBAL VARIABLES ---
let gameDatabase = [];
let allGamesDatabase = [];
let heroFeaturedGames = [];

let recentlyPlayedIds = JSON.parse(localStorage.getItem('recentlyPlayed')) || [];
let favoriteIds = JSON.parse(localStorage.getItem('favoriteGames')) || [];
let currentSlide = 0;

// --- INITIALIZATION ---
window.onload = async function() {
    const slideContainer = document.getElementById('slideContainer');
    
    // 1. Tampilkan loading di layar
    if (slideContainer) {
        slideContainer.innerHTML = `<h2 style="color:white; text-align:center; padding: 100px 20px;">Menghubungkan ke API Slots Launch...</h2>`;
    }

    // 2. Fetch data
    await fetchGamesFromAPI();

    // 3. Jika gagal/kosong, hentikan proses (pesan error sudah ditangani di dalam fetch)
    if (gameDatabase.length === 0) {
        return; 
    }

    // Bersihkan layar loading
    if (slideContainer) slideContainer.innerHTML = '';

    // 4. Render semua komponen jika data berhasil didapat
    initHeroSlider();
    initSearch(); 
    renderHistory();
    renderCatalog(gameDatabase, 'cardsPopularContainer', 10); 
    renderCatalog(gameDatabase, 'cardsPragmaticContainer', 15);
    initDragToScroll();
    
    // Fitur tombol View All
    let isShowingAllPopular = false;
    const btnPopular = document.getElementById('viewAllPopularBtn');
    const containerPopular = document.getElementById('cardsPopularContainer');
    if(btnPopular) {
        btnPopular.addEventListener('click', () => {
            if (!isShowingAllPopular) {
                renderCatalog(gameDatabase.slice(0, 20), 'cardsPopularContainer', 20);
                containerPopular.classList.add('grid-view'); 
                btnPopular.innerText = "Show Less Popular <";
            } else {
                renderCatalog(gameDatabase, 'cardsPopularContainer', 10); 
                containerPopular.classList.remove('grid-view'); 
                btnPopular.innerText = "View More ›";
                containerPopular.parentElement.scrollIntoView({ behavior: 'smooth' });
            }
            isShowingAllPopular = !isShowingAllPopular;
        });
    }

    let isShowingAllPragmatic = false;
    const btnPragmatic = document.getElementById('viewAllPragmaticBtn');
    const containerPragmatic = document.getElementById('cardsPragmaticContainer');
    if(btnPragmatic) {
        btnPragmatic.addEventListener('click', () => {
            if (!isShowingAllPragmatic) {
                renderCatalog(gameDatabase, 'cardsPragmaticContainer', gameDatabase.length); 
                containerPragmatic.classList.add('grid-view'); 
                btnPragmatic.innerText = "Show Less Games <";
            } else {
                renderCatalog(gameDatabase, 'cardsPragmaticContainer', 15); 
                containerPragmatic.classList.remove('grid-view'); 
                btnPragmatic.innerText = "View More ›";
                containerPragmatic.parentElement.scrollIntoView({ behavior: 'smooth' });
            }
            isShowingAllPragmatic = !isShowingAllPragmatic;
        });
    }
};

// --- FUNGSI MENGAMBIL DATA API DENGAN ERROR HANDLING VISUAL ---
async function fetchGamesFromAPI() {
    const slideContainer = document.getElementById('slideContainer');
    
    try {
        const response = await fetch("https://api.slotslaunch.com/v1/games?provider=pragmatic", {
            method: "GET",
            headers: {
                "Authorization": "Bearer dmjtmb2rRCJP20z2nT0ULG5qkO6wIy9tIxr3gs82KzuPMgGiYu",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        });

        // Jika API menolak (401 Unauthorized, 403 Forbidden, 404 Not Found)
        if (!response.ok) {
            console.error("API Error Response:", response);
            if (slideContainer) {
                slideContainer.innerHTML = `<h2 style="color:#ff4444; text-align:center; padding: 100px 20px;">API DITOLAK (Status: ${response.status})<br><span style="font-size:16px; color:#ccc;">Pastikan domain Anda sudah disetujui di whitelist Slots Launch dan API Key valid.</span></h2>`;
            }
            return;
        }

        const data = await response.json();
        
        // Coba mencari array game di berbagai kemungkinan struktur respon JSON
        let apiGames = data;
        if (data.data && Array.isArray(data.data)) apiGames = data.data;
        else if (data.games && Array.isArray(data.games)) apiGames = data.games;
        else if (data.items && Array.isArray(data.items)) apiGames = data.items;
        else if (data.response && Array.isArray(data.response)) apiGames = data.response;
        else if (data.response && data.response.games && Array.isArray(data.response.games)) apiGames = data.response.games;

        // Jika data masih bukan array, tampilkan pesan error struktur
        if (!Array.isArray(apiGames)) {
            console.log("Response aseli dari API:", data);
            if (slideContainer) {
                slideContainer.innerHTML = `<h2 style="color:#ffdd00; text-align:center; padding: 100px 20px;">STRUKTUR API TIDAK DIKENALI<br><span style="font-size:16px; color:#ccc;">Mohon tekan F12 lalu lihat Console untuk melihat format data aslinya.</span></h2>`;
            }
            return;
        }

        // Mapping Data API ke Variabel
        gameDatabase = apiGames.map(game => ({
            id: game.game_code || game.id || game.slug || "unknown", 
            name: game.game_name || game.name || game.title || "Unknown Game",
            rtp: game.rtp || "96.50%", 
            volatility: game.volatility || "High", 
            desc: game.description || "Pragmatic Play Slot Demo."
        }));

        allGamesDatabase = [...gameDatabase];
        
        if (gameDatabase.length >= 4) {
            heroFeaturedGames = [gameDatabase[0], gameDatabase[1], gameDatabase[2], gameDatabase[3]];
        } else {
            heroFeaturedGames = [...gameDatabase];
        }

    } catch (error) {
        // Error koneksi / CORS
        console.error("Koneksi API Gagal / CORS Blocked:", error);
        if (slideContainer) {
            slideContainer.innerHTML = `<h2 style="color:#ff4444; text-align:center; padding: 100px 20px;">GAGAL MENGHUBUNGI API<br><span style="font-size:16px; color:#ccc;">Terjadi masalah CORS (Cross-Origin) atau koneksi internet terputus. Cek Console (F12) untuk detailnya.</span></h2>`;
        }
    }
}

// --- AJAX SEARCH FEATURE ---
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    if(!searchInput || !searchResults) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        searchResults.innerHTML = '';

        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }

        const results = allGamesDatabase.filter(g => g.name.toLowerCase().includes(query)).slice(0, 10);

        if (results.length > 0) {
            searchResults.style.display = 'flex';
            results.forEach(game => {
                const providerName = "Pragmatic Play";
                const searchQuery = providerName + " " + game.name + " slot poster";
                const proxyUrl = "https://tse2.mm.bing.net/th?q=" + encodeURIComponent(searchQuery) + "&w=100&h=100&c=7&rs=1&p=0&dpr=1&pid=1.7";

                const a = document.createElement('a');
                a.className = 'search-result-item';
                a.href = 'game/' + slugify(game.name) + '.html';
                
                a.addEventListener('click', () => saveHistoryOnly(game.id));
                
                a.innerHTML = `
                    <img src="${proxyUrl}" alt="${game.name}">
                    <div class="info">
                        <span class="title">${game.name}</span>
                        <span class="provider">${providerName}</span>
                    </div>
                `;
                searchResults.appendChild(a);
            });
        } else {
            searchResults.style.display = 'flex';
            searchResults.innerHTML = '<div class="search-result-item"><span class="title" style="color:var(--text-muted)">Game not found</span></div>';
        }
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-box')) {
            searchResults.style.display = 'none';
        }
    });
    
    searchInput.addEventListener('focus', () => {
        if(searchInput.value.trim().length >= 2 && searchResults.innerHTML !== '') {
             searchResults.style.display = 'flex';
        }
    });
}

// --- FAVORITES FEATURE ---
function toggleFavorite(gameId) {
    const index = favoriteIds.indexOf(gameId);
    let isLoved = false;
    
    if (index === -1) {
        favoriteIds.unshift(gameId); 
        isLoved = true;
    } else {
        favoriteIds.splice(index, 1); 
        isLoved = false;
    }
    
    localStorage.setItem('favoriteGames', JSON.stringify(favoriteIds));
    return isLoved;
}

function renderHistory() {
    const historySection = document.getElementById('historySection');
    if(!historySection) return;
    
    if (recentlyPlayedIds.length > 0) {
        historySection.style.display = 'block';
        const historyGames = recentlyPlayedIds.map(id => allGamesDatabase.find(g => g.id === id)).filter(g => g);
        renderCatalog(historyGames, 'cardsHistoryContainer', 10);
    } else {
        historySection.style.display = 'none';
    }
}

function clearHistory() {
    localStorage.removeItem('recentlyPlayed');
    recentlyPlayedIds = [];
    renderHistory();
}

function initHeroSlider() {
    const slideContainer = document.getElementById('slideContainer');
    const indicatorsContainer = document.getElementById('sliderIndicators');
    
    if(!slideContainer || !indicatorsContainer || heroFeaturedGames.length === 0) return;
    
    slideContainer.innerHTML = '';
    indicatorsContainer.innerHTML = '';

    heroFeaturedGames.forEach((game, index) => {
        const providerName = "Pragmatic Play";
        const searchQuery = providerName + " " + game.name + " cinematic wallpaper hd";
        const proxyUrl = "https://tse2.mm.bing.net/th?q=" + encodeURIComponent(searchQuery) + "&w=1920&h=1080&c=7&rs=1&p=0&dpr=1&pid=1.7";
        
        const slide = document.createElement('div');
        slide.className = `hero-slide ${index === 0 ? 'active' : ''}`;
        slide.style.backgroundImage = `url('${proxyUrl}')`;
        slide.innerHTML = `
            <div class="hero-slide-overlay">
                <div class="trending-badge">Trending</div>
                <h2 class="hero-slide-title">${game.name}</h2>
                <p class="hero-slide-desc">${game.desc}</p>
                <a href="game/${slugify(game.name)}.html" class="hero-play-btn" onclick="saveHistoryOnly('${game.id}')">
                    ▶ PLAY DEMO
                </a>
            </div>
        `;
        slideContainer.appendChild(slide);

        const dot = document.createElement('div');
        dot.className = `indicator-dot ${index === 0 ? 'active' : ''}`;
        indicatorsContainer.appendChild(dot);
    });

    setInterval(() => {
        const slides = document.querySelectorAll('.hero-slide');
        const dots = document.querySelectorAll('.indicator-dot');
        if(slides.length === 0) return;
        
        slides[currentSlide].classList.remove('active');
        dots[currentSlide].classList.remove('active'); 
        
        currentSlide = (currentSlide + 1) % slides.length;
        
        slides[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active'); 
    }, 5000);
}

function renderCatalog(database, containerId, limit) {
    const container = document.getElementById(containerId);
    if(!container) return;
    
    container.innerHTML = '';
    const gamesToRender = database.slice(0, limit);

    gamesToRender.forEach(game => {
        const card = document.createElement('a');
        card.className = 'game-card';
        card.href = 'game/' + slugify(game.name) + '.html';
        
        const providerName = "Pragmatic Play";
        const searchQuery = providerName + " " + game.name + " slot poster";
        const proxyUrl = "https://tse2.mm.bing.net/th?q=" + encodeURIComponent(searchQuery) + "&w=400&h=600&c=7&rs=1&p=0&dpr=1&pid=1.7";
        const fallbackUrl = `https://placehold.co/400x600/141519/e50914?font=Montserrat&text=${encodeURIComponent(game.name)}`;
        
        const randomRating = (Math.random() * (9.5 - 6.0) + 6.0).toFixed(1);

        const isLoved = favoriteIds.includes(game.id);
        const heartClass = isLoved ? "heart-icon loved" : "heart-icon";

        card.innerHTML = `
            <div class="game-card-thumb">
                <div class="top-badges">
                    <div class="${heartClass}" data-id="${game.id}">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
                    </div>
                    <div class="rating-badge">★ ${randomRating}</div>
                </div>
                <img src="${proxyUrl}" alt="${game.name}" onerror="this.onerror=null; this.src='${fallbackUrl}';">
            </div>
            <div class="game-card-info">
                <h3>${game.name}</h3>
                <div class="provider-tag">2026 • ${providerName}</div>
            </div>
        `;

        card.addEventListener('click', (e) => {
            if(e.target.closest('.heart-icon')) return; 
            saveHistoryOnly(game.id);
        });

        const heartBtn = card.querySelector('.heart-icon');
        heartBtn.addEventListener('click', (e) => {
            e.preventDefault(); 
            e.stopPropagation(); 

            const isNowLoved = toggleFavorite(game.id);
            
            document.querySelectorAll(`.heart-icon[data-id="${game.id}"]`).forEach(icon => {
                if(isNowLoved) {
                    icon.classList.add('loved');
                } else {
                    icon.classList.remove('loved');
                }
            });
        });

        container.appendChild(card);
    });
}

function initDragToScroll() {
    const containers = document.querySelectorAll('.cards-container');
    containers.forEach(container => {
        let isDown = false; let startX; let scrollLeft;
        container.addEventListener('mousedown', (e) => { if(container.classList.contains('grid-view')) return; isDown = true; container.classList.add('active'); startX = e.pageX - container.offsetLeft; scrollLeft = container.scrollLeft; });
        container.addEventListener('mouseleave', () => { isDown = false; container.classList.remove('active'); });
        container.addEventListener('mouseup', () => { isDown = false; container.classList.remove('active'); });
        container.addEventListener('mousemove', (e) => { if (!isDown || container.classList.contains('grid-view')) return; e.preventDefault(); const x = e.pageX - container.offsetLeft; const walk = (x - startX) * 2; container.scrollLeft = scrollLeft - walk; });
    });
}

function saveHistoryOnly(gameId) {
    recentlyPlayedIds = recentlyPlayedIds.filter(id => id !== gameId); 
    recentlyPlayedIds.unshift(gameId); 
    if (recentlyPlayedIds.length > 10) recentlyPlayedIds.pop(); 
    localStorage.setItem('recentlyPlayed', JSON.stringify(recentlyPlayedIds));
}