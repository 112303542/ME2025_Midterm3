// 開啟與關閉Modal
function open_input_table() {
    document.getElementById("addModal").style.display = "block";
    const dateInput = document.getElementById("product_date");
    if (dateInput) {
        dateInput.valueAsDate = new Date();
    }
}
function close_input_table() {
    document.getElementById("addModal").style.display = "none";
}

function delete_data(value) {
    // 發送 DELETE 請求到後端
    fetch(`/product?order_id=${value}`, {
        method: "DELETE",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("伺服器回傳錯誤");
        }
        return response.json(); // 假設後端回傳 JSON 格式資料
    })
    .then(result => {
        console.log(result); // 在這裡處理成功的回應
        close_input_table(); // 關閉 modal
        location.assign('/'); // 重新載入頁面
    })
    .catch(error => {
        console.error("發生錯誤：", error);
    });
}

function selectCategory() {
    // TODO: Fetch product list by category
    const category = document.getElementById("category").value;
    const productSelect = document.getElementById("product_name");
    fetch(`/product?category=${category}`)
        .then(response => response.json())
        .then(data => {
            // 清空目前的商品選項
            productSelect.innerHTML = "";
            
            // 將後端回傳的 product list 逐一加入下拉選單
            // 假設後端回傳格式為 { "product": ["商品A", "商品B"] }
            if (data.product && Array.isArray(data.product)) {
                data.product.forEach(prodName => {
                    const option = document.createElement("option");
                    option.value = prodName;
                    option.text = prodName;
                    productSelect.add(option);
                });
            }

            // 更新完商品列表後，自動選取第一個商品並更新價格
            selectProduct();
        })
        .catch(error => console.error("Error fetching category:", error));
}

function selectProduct() {
    // TODO: Fetch price by product name
    const productName = document.getElementById("product_name").value;
    
    // 如果沒有選取商品則不執行
    if (!productName) return;

    // 發送請求給後端取得該商品的價格
    fetch(`/product?product=${productName}`)
        .then(response => response.json())
        .then(data => {
            // 更新單價欄位
            // 假設後端回傳格式為 { "price": 100 }
            const priceField = document.getElementById("price");
            if (priceField) {
                priceField.value = data.price;
            }
            
            // 更新完單價後，重新計算小計
            countTotal();
        })
        .catch(error => console.error("Error fetching price:", error));
}

function countTotal() {
    // TODO: Calculate total price
    const price = parseFloat(document.getElementById("price").value) || 0;
    const amount = parseInt(document.getElementById("product_amount").value) || 0;
    
    // 計算總價
    const total = price * amount;
    
    // 更新小計欄位
    const totalField = document.getElementById("product_total");
    if (totalField) {
        totalField.value = total;
    }
}