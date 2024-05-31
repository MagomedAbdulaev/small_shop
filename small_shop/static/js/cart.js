const cart_add = document.querySelectorAll('.products__card .cart_add');  // кнопки "добавить в корзину"
const cart_remove = document.querySelectorAll('.products__card .cart_remove');  // кнопки "удалить из корзины"
function ActionsCart(array, action){
    for(let btn of array){
        btn.addEventListener('click', ()=>{
            let btn_id_obj = {
                'id': btn.dataset.setId,
                'action': action,
            };
            fetch('/cart_fetch/',{
               method: 'POST',
               headers: {
                   'X-CSRFToken': csrf_token
               },
               mode: 'same-origin',
               body: JSON.stringify(btn_id_obj),
            })
            .then(response => response.json())
            .then(result => {
                if(action === 'add'){
                    let product_added = document.querySelector('.product_added_container');
                    product_added.style.display = 'flex';
                    const timer = setTimeout(() => {
                        product_added.style.display = 'none';
                    }, 10000)
                }
                else if(action === 'remove'){
                    let products = document.querySelectorAll('.products .products__card');
                    for(let prod of products){
                        if(prod.dataset.setId === result['remove_product_id']){
                            prod.style.display = 'none';
                            break;
                        }
                    }
                }
                CountCart();
            })
        });
    }
}
ActionsCart(cart_add, 'add')
ActionsCart(cart_remove, 'remove')
