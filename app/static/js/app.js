document.addEventListener("DOMContentLoaded", () => {
    fetchProducts();
    document.getElementById("add-product-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const targetPrice = document.getElementById("prod-target").value;
        await fetch("/api/products/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                product_name: document.getElementById("prod-name").value,
                product_url: document.getElementById("prod-url").value,
                website_name: document.getElementById("prod-site").value,
                target_price: targetPrice ? parseFloat(targetPrice) : null
            })
        });
        fetchProducts();
        e.target.reset();
    });
});

async function fetchProducts() {
    const res = await fetch("/api/products/");
    const products = await res.json();
    const tbody = document.getElementById("product-table-body");
    tbody.innerHTML = products.map(p => `
        <tr>
            <td>${p.product_name}</td>
            <td>${p.website_name}</td>
            <td>₹${p.current_price}</td>
            <td>${p.target_price ? '₹' + p.target_price : 'N/A'}</td>
            <td><button class="btn btn-sm btn-danger" onclick="del(${p.id})">X</button></td>
        </tr>
    `).join("");
}

async function del(id) {
    await fetch(`/api/products/${id}`, { method: "DELETE" });
    fetchProducts();
}
