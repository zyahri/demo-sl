function startDemo(gameUrl) {
            document.getElementById('playGate').style.opacity = '0';
            setTimeout(() => {
                document.getElementById('playGate').style.display = 'none';
                // Masukkan URL asli yang dikirim dari HTML saat tombol diklik
                document.getElementById('gameFrame').src = gameUrl;
            }, 500); // efek transisi
        }

        function reloadIframe() {
            var iframe = document.getElementById('gameFrame');
            // Hanya reload jika src bukan about:blank (sudah mulai main)
            if (iframe.src !== "about:blank" && iframe.src !== window.location.href) {
                iframe.src = iframe.src; 
            }
        }

        function toggleFullscreen() {
            var elem = document.getElementById("gameContainer");
            if (!document.fullscreenElement) {
                elem.requestFullscreen().catch(err => console.log(err));
            } else {
                document.exitFullscreen();
            }
        }

        // Logika Untuk Slider Drag Kiri Kanan
        document.addEventListener('DOMContentLoaded', () => {
            const container = document.getElementById('cardsSlider');
            if(!container) return;
            
            let isDown = false; 
            let startX; 
            let scrollLeft;

            container.addEventListener('mousedown', (e) => { 
                isDown = true; 
                container.classList.add('active'); 
                startX = e.pageX - container.offsetLeft; 
                scrollLeft = container.scrollLeft; 
            });
            container.addEventListener('mouseleave', () => { 
                isDown = false; 
                container.classList.remove('active'); 
            });
            container.addEventListener('mouseup', () => { 
                isDown = false; 
                container.classList.remove('active'); 
            });
            container.addEventListener('mousemove', (e) => { 
                if (!isDown) return; 
                e.preventDefault(); 
                const x = e.pageX - container.offsetLeft; 
                const walk = (x - startX) * 2; // kecepatan geser
                container.scrollLeft = scrollLeft - walk; 
            });
        });