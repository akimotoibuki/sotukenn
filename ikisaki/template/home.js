document.addEventListener("DOMContentLoaded", () => {
    // ▼ ジャンル切り替え
    const toggleButton = document.getElementById("toggle-genre");
    const extraGenres = document.getElementById("extra-genres");

    toggleButton.addEventListener("click", () => {
        extraGenres.classList.toggle("hidden");
        toggleButton.textContent = extraGenres.classList.contains("hidden") ? "▶" : "◀";
    });

    // ▼ カレンダー生成
    const calendar = document.getElementById("calendar");
    const today = new Date();
    const year = today.getFullYear();
    const days = ["日", "月", "火", "水", "木", "金", "土"];
    let html = `<h2>${year}年のカレンダー</h2>`;

    for (let month = 0; month < 12; month++) {
        const firstDay = new Date(year, month, 1).getDay();
        const lastDate = new Date(year, month + 1, 0).getDate();

        html += `<div class="month-block"><h3>${month + 1}月</h3><table><tr>`;
        for (let d of days) html += `<th>${d}</th>`;
        html += "</tr><tr>";

        for (let i = 0; i < firstDay; i++) html += "<td></td>";
        for (let date = 1; date <= lastDate; date++) {
            const cellId = `${year}-${month + 1}-${date}`;
            html += `<td id="${cellId}" class="calendar-cell">${date}</td>`;
            if ((date + firstDay) % 7 === 0) html += "</tr><tr>";
        }
        html += "</tr></table></div>";
    }

    calendar.innerHTML = html;

    // ▼ 書き込み＋削除機能
    document.querySelectorAll(".calendar-cell").forEach(cell => {
        cell.addEventListener("click", () => {
            const memo = prompt("予定やスポット名を入力してください：");
            if (memo) {
                const memoDiv = document.createElement("div");
                memoDiv.className = "memo";
                memoDiv.textContent = memo;

                memoDiv.addEventListener("click", (e) => {
                    e.stopPropagation();
                    if (confirm("このメモを削除しますか？")) {
                        memoDiv.remove();
                    }
                });

                cell.appendChild(memoDiv);
            }
        });
    });
});