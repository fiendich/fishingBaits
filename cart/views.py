from django.shortcuts import render, redirect
from catalog.models import Lure, Color
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import OrderForm
from .models import CartItem

def cart(request):
    cart_items = get_cart_items(request)
    total_price = calculate_total_price(cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id, color_id):
    if request.method == 'POST':
        # Получите выбранный товар и цвет из базы данных
        product = Lure.objects.get(id=product_id)
        color = Color.objects.get(id=color_id)

        # Проверяем, есть ли уже такой товар с таким цветом в корзине
        cart_item = CartItem.objects.filter(product=product, color=color).first()

        if cart_item:
            # Если товар уже есть в корзине, увеличиваем количество на 1
            cart_item.quantity += 1
            cart_item.save()
        else:
            # Если товара еще нет в корзине, создаем новый элемент корзины
            cart_item = CartItem(product=product, color=color, quantity=1)
            cart_item.save()

        # Обновляем данные в сессии
        cart_items = request.session.get('cart_items', [])
        if cart_item.id not in cart_items:
            cart_items.append(cart_item.id)
        request.session['cart_items'] = cart_items

        return redirect('cart')


def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        # Получите элемент корзины по его идентификатору
        cart_item = CartItem.objects.get(id=cart_item_id)
        # Удалите элемент корзины
        cart_item.delete()

        # Удалите элемент корзины из сессии
        cart_items = request.session.get('cart_items', [])
        # Удалите идентификатор элемента корзины из списка
        if cart_item_id in cart_items:
            cart_items.remove(cart_item_id)
        # Сохраните обновленный список идентификаторов элементов корзины в сессии
        request.session['cart_items'] = cart_items

        return redirect('cart')


def update_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')
        # Получите элемент корзины по его идентификатору
        cart_item = CartItem.objects.get(id=cart_item_id)
        # Обновите количество товара в элементе корзины
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart')


def calculate_total_price(cart_items):
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.product.price * cart_item.quantity
    return total_price


def get_cart_items(request):
    cart_items = request.session.get('cart_items', [])
    return CartItem.objects.filter(id__in=cart_items)


def order_view(request):
    cart_items = get_cart_items(request)
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Отправить письмо с информацией о заказе
            send_order_email(form.cleaned_data, cart_items)

            # Очистить корзину после успешной отправки заказа
            clear_cart(request)

            # Отображение страницы подтверждения заказа или перенаправление на другую страницу
            return render(request, 'order_confirmation.html')

    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'order.html', context)


def send_order_email(order_data, cart_items):
    # Получите информацию о заказе и создайте текст письма
    email_subject = 'Новый заказ'
    email_message = f'''
    Новый заказ:

    ФИО: {order_data['full_name']}
    Номер телефона: {order_data['phone_number']}
    Email: {order_data['email']}
    Адрес: {order_data['address']}

    Содержимое корзины:
    '''
    for cart_item in cart_items:
        email_message += f'- {cart_item.product.name} ({cart_item.color.name}): {cart_item.product.price} BYN * ' \
                         f'{cart_item.quantity} = {cart_item.product.price*cart_item.quantity}\n'
    email_message += f'(Полная стоимость: {calculate_total_price(cart_items)})'
    # Отправить письмо
    send_mail(email_subject, email_message, 'krfishingbaits@gmail.com', ['krfishingbaits@gmail.com'])


def clear_cart(request):
    # Очистить корзину
    request.session['cart_items'] = []
