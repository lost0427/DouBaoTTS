// 主题切换功能
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle.querySelector('i');
    
    // 检查本地存储的主题设置
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        themeIcon.textContent = '☀️';
    }
    
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        
        if (document.body.classList.contains('dark-mode')) {
            themeIcon.textContent = '☀️';
            localStorage.setItem('theme', 'dark');
        } else {
            themeIcon.textContent = '🌙';
            localStorage.setItem('theme', 'light');
        }
    });

    // 表单提交处理
    document.getElementById('urlForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const url = document.getElementById('urlInput').value;
        const submitBtn = document.getElementById('submitBtn');
        const loading = document.getElementById('loading');
        const result = document.getElementById('result');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');

        // 重置界面
        submitBtn.disabled = true;
        loading.style.display = 'block';
        result.innerHTML = '';
        progressBar.style.width = '0%';
        progressText.textContent = '0%';

        try {
            // 模拟进度条动画
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 10;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                }
                progressBar.style.width = `${progress}%`;
                progressText.textContent = `${Math.round(progress)}%`;
            }, 200);

            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();

            clearInterval(interval);
            progressBar.style.width = '100%';
            progressText.textContent = '100%';

            if (data.code === 1) {
                const baseUrl = window.location.origin;
                let html = '<div class="result success"><h3>转换成功！</h3>';
                html += '<div class="audio-list">';
                data.audio_urls.forEach((audio_url, index) => {
                    const fullUrl = baseUrl + audio_url;
                    html += `<div class="audio-item">
                        <p><strong>段落 ${index + 1}:</strong></p>
                        <audio controls>
                            <source src="${audio_url}" type="audio/mpeg">
                            您的浏览器不支持音频播放。
                        </audio>
                        <button class="copy-button" data-url="${fullUrl}">复制直链</button>
                    </div>`;
                });
                html += '</div></div>';
                result.innerHTML = html;

                // 添加复制按钮的事件监听器
                const copyButtons = document.querySelectorAll('.copy-button');
                copyButtons.forEach(button => {
                    button.addEventListener('click', function() {
                        const urlToCopy = this.getAttribute('data-url');
                        navigator.clipboard.writeText(urlToCopy).then(() => {
                            const originalText = this.textContent;
                            this.textContent = '已复制!';
                            setTimeout(() => {
                                this.textContent = originalText;
                            }, 2000);
                        }).catch(err => {
                            console.error('Failed to copy: ', err);
                        });
                    });
                });
            } else {
                result.innerHTML = `<div class="result error"><p>错误: ${data.message}</p></div>`;
            }
        } catch (error) {
            result.innerHTML = `<div class="result error"><p>请求失败: ${error.message}</p></div>`;
        } finally {
            submitBtn.disabled = false;
            loading.style.display = 'none';
        }
    });
});
