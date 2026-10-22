// Chart.js global defaults
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.borderColor = 'rgba(255,255,255,0.05)';

// Base chart options helper
function chartBaseOptions(overrides = {}) {
    return Object.assign({
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: { color: '#cbd5e1', usePointStyle: true, pointStyle: 'circle', padding: 14 }
            },
            tooltip: {
                backgroundColor: 'rgba(15,17,23,0.95)',
                titleColor: '#f1f5f9',
                bodyColor: '#cbd5e1',
                borderColor: 'rgba(255,255,255,0.1)',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 8,
                displayColors: true,
                boxPadding: 4
            }
        },
        scales: {
            x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#94a3b8' } }
        }
    }, overrides);
}

// Sidebar toggle for mobile
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    if (menuToggle) {
        menuToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
    }

    // Number formatting helpers (global)
    window.formatCurrency = (val) => '$' + Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    window.formatNumber = (val) => Number(val).toLocaleString('en-US');
    window.formatPercent = (val) => Number(val).toFixed(2) + '%';

    // Animate progress bars on load
    const fills = document.querySelectorAll('.ref-bar .fill, .share-bar .fill, .performance-bar .fill, .conv-bar .fill');
    fills.forEach(fill => {
        const w = fill.style.width;
        fill.style.width = '0';
        setTimeout(() => { fill.style.width = w; }, 100);
    });

    // Animate KPI values (count up)
    document.querySelectorAll('.kpi-value').forEach(el => {
        const text = el.textContent;
        const numMatch = text.match(/[\d,.]+/);
        if (!numMatch) return;
        const isCurrency = text.includes('$');
        const target = parseFloat(numMatch[0].replace(/,/g, ''));
        if (isNaN(target)) return;
        let current = 0;
        const steps = 30;
        const inc = target / steps;
        const suffix = text.split(numMatch[0])[1] || '';
        const prefix = isCurrency ? '$' : '';
        let step = 0;
        const timer = setInterval(() => {
            step++;
            current += inc;
            if (step >= steps) {
                current = target;
                clearInterval(timer);
            }
            const display = isCurrency
                ? current.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                : Math.floor(current).toLocaleString('en-US');
            el.textContent = prefix + display + suffix;
        }, 20);
    });
});

// Close sidebar on outside click (mobile)
document.addEventListener('click', function(e) {
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.getElementById('menuToggle');
    if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('open')) {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    }
});

// Chart.js global defaults
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.borderColor = 'rgba(255,255,255,0.05)';

document.addEventListener('DOMContentLoaded', function() {
    // Animate progress bars on load
    const fills = document.querySelectorAll('.share-bar .fill, .performance-bar .fill');
    fills.forEach(fill => {
        const w = fill.style.width;
        fill.style.width = '0';
        setTimeout(() => { fill.style.width = w; }, 100);
    });
});