// 導航列滾動效果
document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('nav');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll <= 0) {
            nav.classList.remove('nav-scrolled');
            return;
        }

        if (currentScroll > lastScroll) {
            // 向下滾動
            nav.style.transform = 'translateY(-100%)';
        } else {
            // 向上滾動
            nav.style.transform = 'translateY(0)';
            nav.classList.add('nav-scrolled');
        }

        lastScroll = currentScroll;
    });
});

// 手機版選單
document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.querySelector('.md\\:hidden');
    const mobileMenu = document.createElement('div');
    mobileMenu.className = 'fixed top-16 right-0 w-64 h-screen bg-white shadow-lg transform translate-x-full transition-transform duration-300 ease-in-out z-40';
    
    // 選單內容
    mobileMenu.innerHTML = `
        <div class="p-4">
            <a href="/internships" class="block py-2 text-gray-700 hover:text-blue-500">找實習</a>
            <a href="/consulting" class="block py-2 text-gray-700 hover:text-blue-500">職涯諮詢</a>
            <a href="/experience" class="block py-2 text-gray-700 hover:text-blue-500">經驗分享</a>
            <div class="border-t my-4"></div>
            <a href="/login" class="block py-2 text-blue-500">登入</a>
            <a href="/register" class="block py-2 text-blue-500">註冊</a>
        </div>
    `;

    document.body.appendChild(mobileMenu);

    menuButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('translate-x-full');
    });

    // 點擊外部關閉選單
    document.addEventListener('click', (e) => {
        if (!menuButton.contains(e.target) && !mobileMenu.contains(e.target)) {
            mobileMenu.classList.add('translate-x-full');
        }
    });
});

// 表單動畫效果
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.form-input');
    
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', () => {
            if (!input.value) {
                input.parentElement.classList.remove('focused');
            }
        });
    });
});

// 平滑滾動
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}); 