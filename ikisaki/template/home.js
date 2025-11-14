document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("toggle-genre");
    const extraGenres = document.getElementById("extra-genres");

    toggleButton.addEventListener("click", () => {
        extraGenres.classList.toggle("hidden");
        toggleButton.textContent = extraGenres.classList.contains("hidden") ? "▶" : "◀";
    });
});