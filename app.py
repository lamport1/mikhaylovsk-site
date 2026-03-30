from flask import Flask
import socket

app = Flask(__name__)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def create_attraction_page(title, description, history, features, address, images=None, current_page=None):
    if not images:
        main_image = f"static/{title.lower().replace(' ', '_').replace('«', '').replace('»', '')}_main.jpg"
        gallery_html = ""
    else:
        main_image = images[0]
        gallery_html = """
            <h2>Фотогалерея</h2>
            <div class="image-gallery">
        """
        for i, img in enumerate(images[1:], 1):
            gallery_html += f'<img src="{img}" alt="{title} - фото {i}" class="gallery-image">'
        gallery_html += "</div>"

    menu_items = [
        ("/", "🏠 Главная страница"),
        ("/alley", "🌳 Аллея Гармония"),
        ("/temple", "⛪ Храм Святого Великомученика Артемия"),
        ("/arch", "🚪 Въездная арка «Михайловск»"),
        ("/michael", "👼 Памятник Архангелу Михаилу"),
        ("/lenin", "🗿 Памятник В. И. Ленину"),
        ("/fountain", "⛲ Фонтан"),
        ("/memorial", "🔥 Мемориальный комплекс «Огонь вечной славы»"),
        ("/museum", "🏛️ Историко-краеведческий музей имени Н. Г. Завгороднего"),
        ("/swallows", "🐦 Аллея «Ласточек»"),
        ("/dendrarium", "🌿 Дендрарий СНИИСХ"),
        ("/admiral", "⚓ Адмиральский парк"),
        ("/rimsky", "🏬 Торгово-выставочный комплекс «Римский мастер»"),
        ("/central_park", "🌲 Центральный парк"),
        ("/admiral_park", "🎠 Парк культуры и отдыха «Адмирал»"),
        ("/victory_park", "🎖️ Парк Победы")
    ]

    menu_html = ""
    for url, name in menu_items:
        if url != current_page:
            menu_html += f'<a href="{url}" class="sidebar-link">{name}</a>'

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            html {{
                scroll-behavior: smooth;
            }}

            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
                overflow-x: hidden;
            }}

            .menu-icon {{
                position: fixed;
                top: 15px;
                left: 15px;
                width: 44px;
                height: 44px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                z-index: 1001;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            }}

            .menu-icon:hover {{
                transform: scale(1.1);
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }}

            .menu-icon .bar {{
                width: 20px;
                height: 2px;
                background: white;
                margin: 2px 0;
                border-radius: 2px;
                transition: all 0.3s ease;
            }}

            .sidebar {{
                position: fixed;
                left: -400px;
                top: 0;
                width: 350px;
                height: 100vh;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.98) 0%, rgba(118, 75, 162, 0.98) 100%);
                backdrop-filter: blur(10px);
                transition: left 0.4s ease;
                z-index: 1000;
                display: flex;
                flex-direction: column;
                padding: 70px 0 20px 0;
                gap: 8px;
                overflow-y: auto;
                box-shadow: 5px 0 25px rgba(0,0,0,0.3);
            }}

            .sidebar.open {{
                left: 0;
            }}

            .overlay {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 999;
                opacity: 0;
                visibility: hidden;
                transition: all 0.4s ease;
            }}

            .overlay.active {{
                opacity: 1;
                visibility: visible;
            }}

            .sidebar-link {{
                color: white;
                font-size: 16px;
                font-weight: 600;
                text-align: left;
                padding: 14px 20px;
                text-decoration: none;
                display: block;
                width: 90%;
                margin: 0 auto;
                transition: all 0.3s ease;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.1);
                border-left: 4px solid transparent;
                position: relative;
                overflow: hidden;
                min-height: 20px;
            }}

            .sidebar-link:before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }}

            .sidebar-link:hover {{
                background: rgba(255, 255, 255, 0.2);
                transform: translateX(10px);
                border-left: 4px solid #fff;
            }}

            .sidebar-link:hover:before {{
                left: 100%;
            }}

            @media (max-width: 768px) {{
                .menu-icon {{
                    top: 10px;
                    left: 10px;
                    width: 44px;
                    height: 44px;
                }}

                .sidebar {{
                    width: 280px;
                    left: -280px;
                }}

                .sidebar-link {{
                    font-size: 15px;
                    padding: 12px 16px;
                }}

                .back-button {{
                    top: 15px;
                    right: 15px;
                    padding: 10px 16px;
                    font-size: 14px;
                }}

                .content-section {{
                    width: 95%;
                    margin: 20px auto;
                    padding: 25px;
                    border-radius: 12px;
                }}

                .content-section h1 {{
                    font-size: 1.8em;
                    padding-bottom: 12px;
                    margin-bottom: 20px;
                }}

                .content-section h2 {{
                    font-size: 1.5em;
                    padding-bottom: 8px;
                    margin-bottom: 15px;
                }}

                .content-section p {{
                    font-size: 1em;
                    line-height: 1.6;
                    margin-bottom: 15px;
                }}

                .content-section ul {{
                    font-size: 1em;
                    line-height: 1.6;
                    margin-bottom: 15px;
                    padding-left: 15px;
                }}

                .main-image {{
                    height: 250px;
                    border-radius: 8px;
                    margin: 15px auto;
                }}

                .image-gallery {{
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 10px;
                    margin: 20px 0;
                }}

                .gallery-image {{
                    height: 150px;
                    border-radius: 6px;
                }}

                .info-card {{
                    padding: 20px;
                    border-radius: 8px;
                    margin: 15px 0;
                }}

                .contact-section {{
                    padding: 40px 15px;
                }}

                .contact-section h2 {{
                    font-size: 2em;
                    margin-bottom: 20px;
                }}

                .contact-section p {{
                    font-size: 1em;
                    margin-bottom: 12px;
                }}

                .nav-menu {{
                    top: 15px;
                    right: 15px;
                    padding: 12px;
                    border-radius: 8px;
                }}

                .nav-menu a {{
                    margin: 8px 0;
                    padding: 10px 15px;
                    font-size: 14px;
                }}

                .hero-container {{
                    height: 50vh;
                    margin-bottom: 30px;
                }}

                .content-overlay h1 {{
                    font-size: 2.5em;
                    margin-bottom: 15px;
                }}

                .content-overlay p {{
                    font-size: 1.2em;
                    max-width: 90%;
                }}

                .scroll-to-top {{
                    bottom: 20px;
                    right: 20px;
                    width: 44px;
                    height: 44px;
                    font-size: 1.3em;
                }}
            }}

            @media (max-width: 480px) {{
                .sidebar {{
                    width: 85%;
                    left: -85%;
                }}

                .content-section {{
                    padding: 20px 15px;
                }}

                .content-section h1 {{
                    font-size: 1.6em;
                }}

                .content-section h2 {{
                    font-size: 1.3em;
                }}

                .hero-container {{
                    height: 40vh;
                }}

                .content-overlay h1 {{
                    font-size: 2em;
                }}

                .content-overlay p {{
                    font-size: 1em;
                }}

                .gallery {{
                    grid-template-columns: 1fr;
                    gap: 15px;
                }}

                .gallery-item {{
                    height: 200px;
                }}
            }}

            .back-button {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: #333;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                z-index: 1000;
                transition: all 0.3s ease;
            }}

            .back-button:hover {{
                background: #555;
                transform: translateY(-2px);
            }}

            .content-section {{
                width: 90%;
                max-width: 1200px;
                margin: 40px auto;
                padding: 50px;
                background-color: white;
                border-radius: 15px;
                box-shadow: 0 5px 25px rgba(0,0,0,0.1);
                opacity: 0;
                transform: translateY(50px);
                transition: all 0.8s ease;
            }}

            .content-section.visible {{
                opacity: 1;
                transform: translateY(0);
            }}

            .content-section h1 {{
                color: #333;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 15px;
                margin-bottom: 25px;
                font-size: 2.5em;
                text-align: center;
            }}

            .content-section h2 {{
                color: #333;
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 10px;
                margin-bottom: 20px;
                font-size: 2em;
            }}

            .content-section p {{
                line-height: 1.8;
                color: #555;
                font-size: 1.1em;
                margin-bottom: 20px;
            }}

            .content-section ul {{
                line-height: 1.8;
                color: #555;
                font-size: 1.1em;
                margin-bottom: 20px;
                padding-left: 20px;
            }}

            .main-image {{
                width: 100%;
                max-width: 800px;
                height: 400px;
                object-fit: cover;
                border-radius: 10px;
                margin: 20px auto;
                display: block;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }}

            .image-gallery {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin: 30px 0;
            }}

            .gallery-image {{
                width: 100%;
                height: 200px;
                object-fit: cover;
                border-radius: 8px;
                transition: transform 0.3s ease;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}

            .gallery-image:hover {{
                transform: scale(1.05);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}

            .info-card {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 4px solid #4CAF50;
            }}

            .info-card h3 {{
                color: #333;
                margin-top: 0;
            }}

            .contact-section {{
                width: 100%;
                max-width: none;
                margin: 0;
                border-radius: 0;
                padding: 60px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }}

            .contact-section h2 {{
                color: white;
                border-bottom: 3px solid rgba(255,255,255,0.5);
                padding-bottom: 15px;
                margin-bottom: 30px;
                font-size: 2.5em;
            }}

            .contact-section p {{
                color: white;
                font-size: 1.2em;
                margin-bottom: 15px;
            }}

            .contact-section strong {{
                color: #fff;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }}

            .scroll-to-top {{
                position: fixed;
                bottom: 30px;
                right: 30px;
                background: #4CAF50;
                color: white;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                text-decoration: none;
                font-size: 1.5em;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
                opacity: 0;
                visibility: hidden;
                z-index: 998;
            }}

            .scroll-to-top.visible {{
                opacity: 1;
                visibility: visible;
            }}

            .scroll-to-top:hover {{
                background: #45a049;
                transform: translateY(-5px);
            }}

            .nav-menu {{
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 999;
                background: rgba(255, 255, 255, 0.9);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }}

            .nav-menu a {{
                display: block;
                margin: 10px 0;
                padding: 8px 15px;
                background: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: all 0.3s ease;
            }}

            .nav-menu a:hover {{
                background: #45a049;
                transform: translateX(-5px);
            }}

            .hero-container {{
                position: relative;
                width: 100%;
                height: 600px;
                border-radius: 0;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                margin-bottom: 50px;
            }}

            .background-image {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                filter: blur(8px);
                transform: scale(1.1);
            }}

            .content-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                background-color: rgba(0, 0, 0, 0.4);
                color: white;
                text-align: center;
                padding: 20px;
                box-sizing: border-box;
            }}

            .content-overlay h1 {{
                font-size: 3.5em;
                margin: 0 0 20px 0;
                text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
            }}

            .content-overlay p {{
                font-size: 1.5em;
                margin: 0;
                text-shadow: 1px 1px 4px rgba(0,0,0,0.7);
                max-width: 80%;
            }}

            .gallery {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }}

            .gallery-item {{
                position: relative;
                height: 250px;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                cursor: pointer;
                background: #f8f9fa;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .gallery-item img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: transform 0.3s ease;
            }}

            .gallery-item:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}

            .gallery-item:hover img {{
                transform: scale(1.05);
            }}
        </style>
    </head>
    <body>
        <div class="overlay" id="overlay" onclick="closeMenu()"></div>

        <div class="menu-icon" onclick="toggleMenu()">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        <div class="sidebar" id="sidebar">
            {menu_html}
        </div>

        <a href="/" class="back-button">← Назад</a>

        <div class="content-section">
            <h1>{title}</h1>

            <img src="{main_image}" alt="{title}" class="main-image" onerror="this.src='https://via.placeholder.com/800x400/4CAF50/white?text={title}'">

            <h2>О достопримечательности</h2>
            <p>{description}</p>

            <div class="info-card">
                <h3>История</h3>
                <p>{history}</p>
            </div>

            <div class="info-card">
                <h3>Особенности</h3>
                <ul>
                    {features}
                </ul>
            </div>

            {gallery_html}

            <div class="info-card">
                <h3>Как добраться</h3>
                <p>{address}</p>
            </div>
        </div>

        <div class="contact-section">
            <h2>Контакты</h2>
            <p><strong>Сайт разработал</strong>: Романенко Глеб Витальевич</p>
            <p><strong>Индивидуальный проект</strong></p>
            <p><strong>МбОУ СОШ 1</strong></p>
            <p><strong>Email:</strong> forestg208@gmail.com</p>
        </div>

        <a href="#" class="scroll-to-top">↑</a>

        <script>
            function toggleMenu() {{
                const sidebar = document.getElementById('sidebar');
                const overlay = document.getElementById('overlay');
                sidebar.classList.toggle('open');
                overlay.classList.toggle('active');
            }}

            function closeMenu() {{
                const sidebar = document.getElementById('sidebar');
                const overlay = document.getElementById('overlay');
                sidebar.classList.remove('open');
                overlay.classList.remove('active');
            }}

            document.querySelectorAll('.sidebar-link').forEach(link => {{
                link.addEventListener('click', closeMenu);
            }});

            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};

            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.classList.add('visible');
                    }}
                }});
            }}, observerOptions);

            document.querySelectorAll('.content-section').forEach(section => {{
                observer.observe(section);
            }});

            const scrollToTopBtn = document.querySelector('.scroll-to-top');

            window.addEventListener('scroll', () => {{
                if (window.pageYOffset > 300) {{
                    scrollToTopBtn.classList.add('visible');
                }} else {{
                    scrollToTopBtn.classList.remove('visible');
                }}
            }});

            scrollToTopBtn.addEventListener('click', (e) => {{
                e.preventDefault();
                window.scrollTo({{
                    top: 0,
                    behavior: 'smooth'
                }});
            }});

            document.addEventListener('touchstart', function() {{}}, {{passive: true}});
        </script>
    </body>
    </html>
    '''

@app.route('/')
def html_text():
    menu_items = [
        ("/alley", "🌳 Аллея Гармония"),
        ("/temple", "⛪ Храм Святого Великомученика Артемия"),
        ("/arch", "🚪 Въездная арка «Михайловск»"),
        ("/michael", "👼 Памятник Архангелу Михаилу"),
        ("/lenin", "🗿 Памятник В. И. Ленину"),
        ("/fountain", "⛲ Фонтан"),
        ("/memorial", "🔥 Мемориальный комплекс «Огонь вечной славы»"),
        ("/museum", "🏛️ Историко-краеведческий музей имени Н. Г. Завгороднего"),
        ("/swallows", "🐦 Аллея «Ласточек»"),
        ("/dendrarium", "🌿 Дендрарий СНИИСХ"),
        ("/admiral", "⚓ Адмиральский парк"),
        ("/rimsky", "🏬 Торгово-выставочный комплекс «Римский мастер»"),
        ("/central_park", "🌲 Центральный парк"),
        ("/admiral_park", "🎠 Парк культуры и отдыха «Адмирал»"),
        ("/victory_park", "🎖️ Парк Победы")
    ]

    menu_html = ""
    for url, name in menu_items:
        menu_html += f'<a href="{url}" class="sidebar-link">{name}</a>'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            html {{
                scroll-behavior: smooth;
            }}

            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
                overflow-x: hidden;
            }}

            .menu-icon {{
                position: fixed;
                top: 15px;
                left: 15px;
                width: 44px;
                height: 44px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                z-index: 1001;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            }}

            .menu-icon:hover {{
                transform: scale(1.1);
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }}

            .menu-icon .bar {{
                width: 20px;
                height: 2px;
                background: white;
                margin: 2px 0;
                border-radius: 2px;
                transition: all 0.3s ease;
            }}

            .sidebar {{
                position: fixed;
                left: -400px;
                top: 0;
                width: 350px;
                height: 100vh;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.98) 0%, rgba(118, 75, 162, 0.98) 100%);
                backdrop-filter: blur(10px);
                transition: left 0.4s ease;
                z-index: 1000;
                display: flex;
                flex-direction: column;
                padding: 70px 0 20px 0;
                gap: 8px;
                overflow-y: auto;
                box-shadow: 5px 0 25px rgba(0,0,0,0.3);
            }}

            .sidebar.open {{
                left: 0;
            }}

            .overlay {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 999;
                opacity: 0;
                visibility: hidden;
                transition: all 0.4s ease;
            }}

            .overlay.active {{
                opacity: 1;
                visibility: visible;
            }}

            .sidebar-link {{
                color: white;
                font-size: 16px;
                font-weight: 600;
                text-align: left;
                padding: 14px 20px;
                text-decoration: none;
                display: block;
                width: 90%;
                margin: 0 auto;
                transition: all 0.3s ease;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.1);
                border-left: 4px solid transparent;
                position: relative;
                overflow: hidden;
                min-height: 20px;
            }}

            .sidebar-link:before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }}

            .sidebar-link:hover {{
                background: rgba(255, 255, 255, 0.2);
                transform: translateX(10px);
                border-left: 4px solid #fff;
            }}

            .sidebar-link:hover:before {{
                left: 100%;
            }}

            @media (max-width: 768px) {{
                .menu-icon {{
                    top: 10px;
                    left: 10px;
                    width: 44px;
                    height: 44px;
                }}

                .sidebar {{
                    width: 280px;
                    left: -280px;
                }}

                .sidebar-link {{
                    font-size: 15px;
                    padding: 12px 16px;
                }}

                .nav-menu {{
                    top: 15px;
                    right: 15px;
                    padding: 12px;
                    border-radius: 8px;
                }}

                .nav-menu a {{
                    margin: 8px 0;
                    padding: 10px 15px;
                    font-size: 14px;
                }}

                .hero-container {{
                    height: 50vh;
                    margin-bottom: 30px;
                }}

                .content-overlay h1 {{
                    font-size: 2.5em;
                    margin-bottom: 15px;
                }}

                .content-overlay p {{
                    font-size: 1.2em;
                    max-width: 90%;
                }}

                .content-section {{
                    width: 95%;
                    margin: 20px auto;
                    padding: 25px;
                    border-radius: 12px;
                }}

                .content-section h2 {{
                    font-size: 1.5em;
                    padding-bottom: 8px;
                    margin-bottom: 15px;
                }}

                .content-section p {{
                    font-size: 1em;
                    line-height: 1.6;
                    margin-bottom: 15px;
                }}

                .gallery {{
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 10px;
                    margin-top: 20px;
                }}

                .gallery-item {{
                    height: 150px;
                    border-radius: 8px;
                }}

                #contact {{
                    padding: 40px 15px;
                }}

                #contact h2 {{
                    font-size: 2em;
                    margin-bottom: 20px;
                }}

                #contact p {{
                    font-size: 1em;
                    margin-bottom: 12px;
                }}

                .scroll-to-top {{
                    bottom: 20px;
                    right: 20px;
                    width: 44px;
                    height: 44px;
                    font-size: 1.3em;
                }}
            }}

            @media (max-width: 480px) {{
                .sidebar {{
                    width: 85%;
                    left: -85%;
                }}

                .hero-container {{
                    height: 40vh;
                }}

                .content-overlay h1 {{
                    font-size: 2em;
                }}

                .content-overlay p {{
                    font-size: 1em;
                }}

                .content-section {{
                    padding: 20px 15px;
                }}

                .content-section h2 {{
                    font-size: 1.3em;
                }}

                .gallery {{
                    grid-template-columns: 1fr;
                    gap: 15px;
                }}

                .gallery-item {{
                    height: 200px;
                }}

                .nav-menu {{
                    display: none;
                }}
            }}

            .hero-container {{
                position: relative;
                width: 100%;
                height: 600px;
                border-radius: 0;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                margin-bottom: 50px;
            }}

            .background-image {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                filter: blur(8px);
                transform: scale(1.1);
            }}

            .content-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                background-color: rgba(0, 0, 0, 0.4);
                color: white;
                text-align: center;
                padding: 20px;
                box-sizing: border-box;
            }}

            .content-overlay h1 {{
                font-size: 3.5em;
                margin: 0 0 20px 0;
                text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
            }}

            .content-overlay p {{
                font-size: 1.5em;
                margin: 0;
                text-shadow: 1px 1px 4px rgba(0,0,0,0.7);
                max-width: 80%;
            }}

            .nav-menu {{
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 999;
                background: rgba(255, 255, 255, 0.9);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }}

            .nav-menu a {{
                display: block;
                margin: 10px 0;
                padding: 8px 15px;
                background: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: all 0.3s ease;
            }}

            .nav-menu a:hover {{
                background: #45a049;
                transform: translateX(-5px);
            }}

            .content-section {{
                width: 90%;
                max-width: 1200px;
                margin: 40px auto;
                padding: 50px;
                background-color: white;
                border-radius: 15px;
                box-shadow: 0 5px 25px rgba(0,0,0,0.1);
                opacity: 0;
                transform: translateY(50px);
                transition: all 0.8s ease;
            }}

            .content-section.visible {{
                opacity: 1;
                transform: translateY(0);
            }}

            .content-section h2 {{
                color: #333;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 15px;
                margin-bottom: 25px;
                font-size: 2.2em;
            }}

            .content-section p {{
                line-height: 1.8;
                color: #555;
                font-size: 1.1em;
                margin-bottom: 20px;
            }}

            .gallery {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }}

            .gallery-item {{
                position: relative;git
                height: 250px;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                cursor: pointer;
                background: #f8f9fa;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .gallery-item img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                transition: transform 0.3s ease;
            }}

            .gallery-item:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}

            .gallery-item:hover img {{
                transform: scale(1.05);
            }}

            #contact {{
                width: 100%;
                max-width: none;
                margin: 0;
                border-radius: 0;
                padding: 60px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }}

            #contact h2 {{
                color: white;
                border-bottom: 3px solid rgba(255,255,255,0.5);
                padding-bottom: 15px;
                margin-bottom: 30px;
                font-size: 2.5em;
            }}

            #contact p {{
                color: white;
                font-size: 1.2em;
                margin-bottom: 15px;
            }}

            #contact strong {{
                color: #fff;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }}

            .scroll-to-top {{
                position: fixed;
                bottom: 30px;
                right: 30px;
                background: #4CAF50;
                color: white;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                text-decoration: none;
                font-size: 1.5em;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
                opacity: 0;
                visibility: hidden;
                z-index: 998;
            }}

            .scroll-to-top.visible {{
                opacity: 1;
                visibility: visible;
            }}

            .scroll-to-top:hover {{
                background: #45a049;
                transform: translateY(-5px);
            }}
        </style>
    </head>
    <body>
        <div class="overlay" id="overlay" onclick="closeMenu()"></div>

        <div class="menu-icon" onclick="toggleMenu()">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        <div class="sidebar" id="sidebar">
            <a href="/" class="sidebar-link">🏠 Главная страница</a>
            {menu_html}
        </div>

        <div class="nav-menu">
            <a href="#about">О городе</a>
            <a href="#attractions">Достопримечательности</a>
            <a href="#gallery">Галерея</a>
            <a href="#contact">Контакты</a>
        </div>

        <div class="hero-container">
            <img src="static/background1.jpeg" alt="Михайловск" class="background-image">
            <div class="content-overlay">
                <h1><b>Михайловск</b></h1>
                <p>Добро пожаловать в прекрасный город</p>
            </div>
        </div>

        <div id="about" class="content-section">
            <h2>О нашем городе</h2>
            <p>Михайловск — это живописный город с богатой историей и культурным наследием. Здесь сочетаются современная инфраструктура и традиционный уклад жизни, создавая уникальную атмосферу для жителей и гостей города.</p>
            <p>Город окружен красивой природой, что делает его привлекательным для любителей пеших прогулок и активного отдыха. В Михайловске развита социальная инфраструктура, есть школы, детские сады, медицинские учреждения и разнообразные магазины.</p>
            <p>Население города составляет около 100 тысяч человек, и с каждным годом Михайловск становится все более привлекательным для жизни и инвестиций.</p>
        </div>

        <div id="attractions" class="content-section">
            <h2>Достопримечательности</h2>
            <p>В нашем городе есть множество интересных мест, которые стоит посетить:</p>
            <ul>
                <li><strong>Исторический центр</strong> с архитектурой XIX века</li>
                <li><strong>Городской парк</strong> с фонтанами и аллеями</li>
                <li><strong>Краеведческий музей</strong> с уникальными экспонатами</li>
                <li><strong>Церковь Святого Михаила</strong> - памятник архитектуры</li>
                <li><strong>Набережная реки</strong> с живописными видами</li>
                <li><strong>Спортивный комплекс</strong> мирового уровня</li>
            </ul>
        </div>

        <div id="gallery" class="content-section">
            <h2>Фотогалерея</h2>
            <p>Посмотрите на красоты нашего города:</p>
            <div class="gallery">
                <div class="gallery-item">
                    <img src="static/scale_1200.jpeg" alt="Центральная площадь">
                </div>
                <div class="gallery-item">
                    <img src="static/2.jpg" alt="Городской парк">
                </div>
                <div class="gallery-item">
                    <img src="static/3.jpg" alt="Исторический музей">
                </div>
                <div class="gallery-item">
                    <img src="static/4.jpeg" alt="Речная набережная">
                </div>
                <div class="gallery-item">
                    <img src="static/5.jpg" alt="Спортивный комплекс">
                </div>
                <div class="gallery-item">
                    <img src="static/6.jpg" alt="Вечерний город">
                </div>
            </div>
        </div>

        <div id="contact" class="content-section">
            <h2>Контакты</h2>
            <p><strong>Сайт разработал</strong>: Романенко Глеб Витальевич</p>
            <p><strong>Индивидуальный проект</strong></p>
            <p><strong>МбОУ СОШ 1</strong></p>
            <p><strong>Email:</strong> forestg208@gmail.com</p>
        </div>

        <a href="#" class="scroll-to-top">↑</a>

        <script>
            function toggleMenu() {{
                const sidebar = document.getElementById('sidebar');
                const overlay = document.getElementById('overlay');
                sidebar.classList.toggle('open');
                overlay.classList.toggle('active');
            }}

            function closeMenu() {{
                const sidebar = document.getElementById('sidebar');
                const overlay = document.getElementById('overlay');
                sidebar.classList.remove('open');
                overlay.classList.remove('active');
            }}

            document.querySelectorAll('.sidebar-link').forEach(link => {{
                link.addEventListener('click', closeMenu);
            }});

            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};

            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.classList.add('visible');
                    }}
                }});
            }}, observerOptions);

            document.querySelectorAll('.content-section').forEach(section => {{
                observer.observe(section);
            }});

            const scrollToTopBtn = document.querySelector('.scroll-to-top');

            window.addEventListener('scroll', () => {{
                if (window.pageYOffset > 300) {{
                    scrollToTopBtn.classList.add('visible');
                }} else {{
                    scrollToTopBtn.classList.remove('visible');
                }}
            }});

            scrollToTopBtn.addEventListener('click', (e) => {{
                e.preventDefault();
                window.scrollTo({{
                    top: 0,
                    behavior: 'smooth'
                }});
            }});

            document.addEventListener('touchstart', function() {{}}, {{passive: true}});
        </script>
    </body>
    </html>
    """

@app.route('/alley')
def alley():
    return create_attraction_page(
        title="Аллея Гармония",
        description="Аллея Гармония - это одно из самых красивых и уютных мест в Михайловске, где природа гармонично сочетается с современным благоустройством. Это излюбленное место прогулок как жителей города, так и его гостей.",
        history="Аллея была создана в 2018 году в рамках программы благоустройства городской среды. Название 'Гармония' было выбрано не случайно - здесь гармонично сочетаются зеленые насаждения, малые архитектурные формы и современное освещение.",
        features="<li>Протяженность аллеи - 350 метров</li><li>Более 50 видов деревьев и кустарников</li><li>Современная система освещения</li><li>Скамейки для отдыха</li><li>Детская игровая площадка</li><li>Фонтаны и цветочные клумбы</li>",
        address="Аллея Гармония расположена в центральной части города Михайловска, рядом с городским парком. Добраться можно на общественном транспорте до остановки 'Центральный парк' или 'Городская администрация'.",
        images=[
            "static/6.jpg",
            "static/7.jpg",
            "static/8.jpg",
        ],
        current_page="/alley"
    )

@app.route('/temple')
def temple():
    return create_attraction_page(
        title="Храм Святого Великомученика Артемия",
        description="Храм Святого Великомученика Артемия - это православный храм в Михайловске, являющийся важным духовным центром города и местом паломничества верующих.",
        history="Храм был построен в 2005 году и освящен в честь святого великомученика Артемия. С тех пор он стал местом притяжения для верующих жителей города и окрестностей.",
        features="<li>Красивая архитектура в русском стиле</li><li>Вместимость до 500 прихожан</li><li>Воскресная школа для детей</li><li>Библиотека православной литературы</li><li>Иконостас ручной работы</li>",
        address="Храм расположен в центральной части города. Адрес: г. Михайловск, ул. Церковная, 1.",
        images=[
            "static/9.jpg",
            "static/10.jpg",
            "static/11.jpg"
        ],
        current_page="/temple"
    )

@app.route('/arch')
def arch():
    return create_attraction_page(
        title="Въездная арка «Михайловск»",
        description="Въездная арка «Михайловск» - это символические ворота города, встречающие всех гостей и жителей. Арка стала визитной карточкой Михайловска.",
        history="Арка была построена в 2010 году к юбилею города. Она символизирует гостеприимство и открытость Михайловска для всех гостей.",
        features="<li>Высота арки - 8 метров</li><li>Современная подсветка в ночное время</li><li>Каменная кладка с декоративными элементами</li><li>Надпись с названием города</li><li>Клумбы с цветами вокруг арки</li>",
        address="Арка расположена на главном въезде в город со стороны федеральной трассы.",
        images=[
            "static/12.jpg",
            "static/13.jpg",
            "static/14.jpg",
        ],
        current_page="/arch"
    )

@app.route('/michael')
def michael():
    return create_attraction_page(
        title="Памятник Архангелу Михаилу",
        description="Памятник Архангелу Михаилу - это величественная скульптура, установленная в честь небесного покровителя города Михайловска.",
        history="Памятник был установлен в 2015 году и освящен духовенством. Архангел Михаил считается защитником и покровителем города.",
        features="<li>Бронзовая скульптура высотой 4 метра</li><li>Мраморное основание</li><li>Художественная подсветка</li><li>Благоустроенная территория вокруг</li><li>Смотровая площадка</li>",
        address="Памятник расположен в центре города, на площади Свободы.",
        images=[
            "static/15.jpg",
            "static/16.jpg",
            "static/17.jpg"
        ],
        current_page="/michael"
    )

@app.route('/lenin')
def lenin():
    return create_attraction_page(
        title="Памятник В. И. Ленину",
        description="Памятник Владимиру Ильичу Ленину - это исторический монумент, сохранившийся с советских времен и являющийся частью культурного наследия города.",
        history="Памятник был установлен в 1970 году в честь 100-летия со дня рождения В. И. Ленина. За годы существования он стал неотъемлемой частью городского ландшафта.",
        features="<li>Бронзовая скульптура в полный рост</li><li>Гранитный постамент</li><li>Историческая ценность</li><li>Ухоженная территория</li><li>Место проведения мероприятий</li>",
        address="Памятник расположен на центральной площади города, перед зданием администрации.",
        images=[
            "static/19.jpg",
            "static/18.jpg"
        ],
        current_page="/lenin"
    )

@app.route('/fountain')
def fountain():
    return create_attraction_page(
        title="Фонтан",
        description="Городской фонтан - это излюбленное место отдыха горожан, особенно в жаркие летние дни. Фонтан с музыкальным и световым сопровождением создает особую атмосферу.",
        history="Фонтан был построен в 2012 году в рамках программы благоустройства центральной площади. С тех пор он стал популярным местом встреч и отдыха.",
        features="<li>Музыкальное сопровождение</li><li>Цветная динамическая подсветка</li><li>Несколько уровней водных струй</li><li>Вечерние световые шоу</li><li>Зона отдыха с лавочками</li>",
        address="Фонтан расположен в центре города, на главной площади.",
        images=[
            "static/20.jpg",
            "static/21.jpg",
            "static/22.jpg",
            "static/23.jpg"
        ],
        current_page="/fountain"
    )

@app.route('/memorial')
def memorial():
    return create_attraction_page(
        title="Мемориальный комплекс «Огонь вечной славы»",
        description="Мемориальный комплекс «Огонь вечной славы» - это священное место памяти о героях Великой Отечественной войны, отдавших жизни за Родину.",
        history="Комплекс был открыт в 1975 году к 30-летию Победы в Великой Отечественной войне. Здесь проводятся памятные мероприятия и возложения цветов.",
        features="<li>Вечный огонь</li><li>Стена памяти с именами героев</li><li>Скульптурная композиция</li><li>Аллея славы</li><li>Место для проведения торжественных мероприятий</li>",
        address="Мемориальный комплекс расположен в парковой зоне в центре города.",
        images=[
            "static/24.jpg",
            "static/25.jpg",
            "static/26.jpg"
        ],
        current_page="/memorial"
    )

@app.route('/museum')
def museum():
    return create_attraction_page(
        title="Историко-краеведческий музей имени Н. Г. Завгороднего",
        description="Музей имени Н. Г. Завгороднего - это хранилище истории и культуры Михайловска, где собраны уникальные экспонаты, рассказывающие о прошлом и настоящем города.",
        history="Музей был основан в 1985 году и назван в честь известного краеведа Н. Г. Завгороднего. За годы работы музей стал важным культурным центром города.",
        features="<li>Более 5000 экспонатов</li><li>Археологическая коллекция</li><li>Этнографический отдел</li><li>Картинная галерея</li><li>Интерактивные экскурсии</li><li>Временные выставки</li>",
        address="Музей расположен в историческом здании в центре города. Адрес: г. Михайловск, ул. Музейная, 15.",
        images=[
            "static/27.jpg",
            "static/28.jpg",
            "static/29.jpg",
            "static/30.jpg"
        ],
        current_page="/museum"
    )

@app.route('/swallows')
def swallows():
    return create_attraction_page(
        title="Аллея «Ласточек»",
        description="Аллея «Ласточек» - это живописная пешеходная зона, украшенная скульптурами ласточек и цветущими растениями. Символизирует весну, обновление и надежду.",
        history="Аллея была создана в 2017 году как подарок городу от местных предпринимателей. Название было выбрано по результатам городского конкурса.",
        features="<li>Скульптуры ласточек из бронзы</li><li>Скамейки для отдыха в виде гнезд</li><li>Цветущие клумбы</li><li>Декоративное освещение</li><li>Детская игровая зона</li>",
        address="Аллея расположена в новом микрорайоне города, рядом с жилыми домами.",
        images=[
            "static/31.jpg",
            "static/32.jpg",
            "static/33.jpg"
        ],
        current_page="/swallows"
    )

@app.route('/dendrarium')
def dendrarium():
    return create_attraction_page(
        title="Дендрарий СНИИСХ",
        description="Дендрарий Северо-Кавказского научно-исследовательского института сельского хозяйства - это уникальный парк с богатой коллекцией растений, являющийся объектом научных исследований и местом отдыха.",
        history="Дендрарий был основан в 1960 году как экспериментальная площадка для изучения адаптации растений к местным климатическим условиям.",
        features="<li>Более 1000 видов растений</li><li>Редкие и исчезающие виды</li><li>Тематические зоны</li><li>Экскурсионные программы</li><li>Научно-исследовательская деятельность</li><li>Зона отдыха</li>",
        address="Дендрарий расположен на территории СНИИСХ. Адрес: г. Михайловск, ул. Научная, 1.",
        images=[
            "static/34.jpg",
            "static/35.jpg",
            "static/36.jpg",
            "static/37.jpg"
        ],
        current_page="/dendrarium"
    )

@app.route('/admiral')
def admiral():
    return create_attraction_page(
        title="Адмиральский парк",
        description="Адмиральский парк - это современная рекреационная зона, названная в честь знаменитых русских адмиралов. Парк сочетает в себе историческую память и современные возможности для отдыха.",
        history="Парк был открыт в 2019 году после масштабной реконструкции. Название было выбрано в честь морской славы России.",
        features="<li>Аллея адмиралов с бюстами</li><li>Детские площадки</li><li>Спортивные зоны</li><li>Искусственный пруд</li><li>Велосипедные дорожки</li><li>Зона для пикников</li>",
        address="Парк расположен в западной части города, рядом с жилым массивом.",
        images=[
            "static/38.jpg",
            "static/39.jpg",
            "static/40.jpg"
        ],
        current_page="/admiral"
    )

@app.route('/rimsky')
def rimsky():
    return create_attraction_page(
        title="Торгово-выставочный комплекс «Римский мастер»",
        description="Торгово-выставочный комплекс «Римский мастер» - это современный многофункциональный центр, объединяющий торговые площади, выставочные залы и культурные пространства.",
        history="Комплекс был построен в 2016 году и стал одним из первых объектов такого масштаба в городе. Название отражает стремление к качеству и мастерству.",
        features="<li>Торговые галереи</li><li>Выставочные залы</li><li>Конференц-залы</li><li>Фуд-корт</li><li>Детская игровая зона</li><li>Подземная парковка</li>",
        address="Комплекс расположен в деловом центре города. Адрес: г. Михайловск, ул. Торговая, 25.",
        images=[
            "static/41.jpg",
            "static/42.jpg",
            "static/43.jpg"
        ],
        current_page="/rimsky"
    )

@app.route('/central_park')
def central_park():
    return create_attraction_page(
        title="Центральный парк",
        description="Центральный парк - это главная зона отдыха Михайловска, любимое место проведения досуга для жителей всех возрастов. Парк сочетает природную красоту с современной инфраструктурой.",
        history="Парк был заложен в 1950-х годах и с тех пор неоднократно реконструировался. Сегодня это современное пространство для отдыха и развлечений.",
        features="<li>Аттракционы для всех возрастов</li><li>Концертная площадка</li><li>Танцплощадка</li><li>Кафе и рестораны</li><li>Прогулочные аллеи</li><li>Спортивные площадки</li>",
        address="Парк расположен в самом центре города, занимает территорию 15 гектаров.",
        images=[
            "static/44.jpg",
            "static/45.jpg",
            "static/46.jpg",
            "static/47.jpg"
        ],
        current_page="/central_park"
    )

@app.route('/admiral_park')
def admiral_park():
    return create_attraction_page(
        title="Парк культуры и отдыха «Адмирал»",
        description="Парк культуры и отдыха «Адмирал» - это современное многофункциональное пространство для активного отдыха, культурных мероприятий и семейного досуга.",
        history="Парк был открыт в 2018 году после масштабной реконструкции стадиона. Название отражает морскую тематику оформления.",
        features="<li>Спортивный стадион</li><li>Детские игровые комплексы</li><li>Веревочный парк</li><li>Скейт-парк</li><li>Летний кинотеатр</li><li>Зона для мероприятий</li>",
        address="Парк расположен в северной части города, рядом с жилыми кварталами.",
        images=[
            "static/48.jpg",
            "static/49.jpg",
            "static/50.jpg"
        ],
        current_page="/admiral_park"
    )

@app.route('/victory_park')
def victory_park():
    return create_attraction_page(
        title="Парк Победы",
        description="Парк Победы - это мемориально-парковый комплекс, посвященный победе в Великой Отечественной войне. Это место памяти, скорби и гордости за подвиг предков.",
        history="Парк был заложен в 1980 году к 35-летию Победы. С тех пор он постоянно развивается и благоустраивается.",
        features="<li>Мемориал воинам-освободителям</li><li>Аллея героев</li><li>Выставка военной техники</li><li>Храм-часовня</li><li>Зона тихого отдыха</li><li>Детская площадка</li>",
        address="Парк расположен в восточной части города, на берегу реки.",
        images=[
            "static/51.jpg",
            "static/52.jpg",
            "static/53.jpg"
        ],
        current_page="/victory_park"
    )

if __name__ == '__main__':
    local_ip = get_local_ip()

    print(f"\n=== Сервер запущен ===")
    print(f"Локальный доступ: http://localhost:5000")
    print(f"Сетевой доступ: http://{local_ip}:5000")
    print(f"=====================\n")

    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)