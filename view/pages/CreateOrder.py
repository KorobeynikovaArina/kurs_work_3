from os import makedirs, path
import shutil
import flet as ft
from services.ClientTypeService import ClientTypeService
from services.OrderService import OrderService
from services.UserService import UserService
from services.StatusService import StatusService
from view.ROUTES import ORDERS, ORDERS_CREATE, LOGIN, ADMIN
import uuid


def order_create(page: ft.Page):
    orderService = OrderService()
    clientTypeService = ClientTypeService()
    userService = UserService()
    statusService = StatusService()
    troute = ft.TemplateRoute(page.route)
    is_update = False
    current_user = userService.get_user_by_token(
        page.client_storage.get("token")
    )
    if not current_user:
        return

    is_admin = userService.is_admin(page.client_storage.get("token"))

    client_types = clientTypeService.get_all()
    statuses = statusService.get_all()

    default_values = {"id": "",
                      "client": "",
                      "client_type": "",
                      "contact": "",
                      "product_type": "",
                      "material_filepath": "",
                      "user": current_user.id,
                      "status": "", }

    if troute.match(ORDERS_CREATE+"/:id"):
        is_update = True
        id = troute.id[1:]
        order = orderService.get_by_id(id)

        default_values["id"] = order.id
        default_values["client"] = order.client
        default_values["client_type"] = order.client_type
        default_values["contact"] = order.contact
        default_values["product_type"] = order.product_type
        default_values["material_filepath"] = order.material_filepath
        default_values["user"] = order.user
        default_values["status"] = order.status

    def logout(e):
        page.client_storage.remove("token")
        page.go(LOGIN)

    def create_order(e):
        uploaded_files_urls = upload_files(e)
        materials = ','.join(uploaded_files_urls)
        if client_input.value == "" or client_type_select.value == "" or contact_input.value == "" or product_type_input.value == "" or status_select.value == "" or materials == "":
            return
        orderService.create(client=client_input.value, client_type=client_type_select.value, contact=contact_input.value,
                            product_type=product_type_input.value, material_filepath=materials, user=current_user.id, status=status_select.value)
        page.go(ORDERS)

    def update_order(e):
        uploaded_files_urls = upload_files(e)
        materials = ','.join(uploaded_files_urls)
        if client_input.value == "" or client_type_select.value == "" or contact_input.value == "" or product_type_input.value == "" or status_select.value == "":
            return
        orderService.update(default_values["id"], client=client_input.value, client_type=client_type_select.value, contact=contact_input.value,
                            product_type=product_type_input.value, material_filepath=materials, user=current_user.id, status=status_select.value)
        page.go(ORDERS)

    def pick_files_result(e: ft.FilePickerResultEvent):
        selected_files_text.value = (
            ", ".join(map(lambda f: f.name, e.files)
                      ) if e.files else "Cancelled!"
        )
        selected_files_text.update()

    def upload_files(e):
        upload_list = []

        if file_picker.result != None and file_picker.result.files != None:
            for f in file_picker.result.files:
                upload_dir = current_user.upload_dir
                if not path.exists(upload_dir):
                    makedirs(upload_dir)
                upload_url = path.join(upload_dir, f"{uuid.uuid4()}_{f.name}")
                upload_list.append(upload_url)
                shutil.copy(f.path, upload_url)
        return [upload_url for upload_url in upload_list]

    def on_submit(e):
        if is_update:
            return update_order(e)
        return create_order(e)

    client_input = ft.TextField(
        value=default_values["client"], hint_text="Client", label="Client", autofocus=True, on_submit=on_submit)

    client_type_select = ft.Dropdown(
        value=default_values["client_type"],
        label="Client type",
        options=[ft.dropdown.Option(key=client_type.id, text=client_type.title) for client_type in client_types])

    contact_input = ft.TextField(
        value=default_values['contact'], hint_text="Contact", label="Contact", on_submit=on_submit)

    product_type_input = ft.TextField(
        value=default_values["product_type"], hint_text="Product type", label="Product type", on_submit=on_submit)

    file_picker = ft.FilePicker(on_result=pick_files_result)
    selected_files_text = ft.Text(value=default_values["material_filepath"])
    select_files_btn = ft.ElevatedButton(text="Pick materials",
                                         icon=ft.icons.UPLOAD_FILE,
                                         on_click=lambda _: file_picker.pick_files(
                                             allow_multiple=True))

    status_select = ft.Dropdown(
        value=default_values["status"],
        label="Status",
        options=[ft.dropdown.Option(key=status.id, text=status.title) for status in statuses])

    create_btn = ft.TextButton(
        text="Create", on_click=create_order, visible=not is_update)
    update_btn = ft.TextButton(
        text="Update", on_click=update_order, visible=is_update)

    logout_btn = ft.TextButton(text="Logout", on_click=logout)
    admin_panel = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN), visible=is_admin)
    home_btn = ft.TextButton(
        text="Home", on_click=lambda e: page.go(ORDERS))

    navbar = ft.Row([logout_btn, admin_panel, home_btn])

    page.overlay.append(file_picker)
    return [navbar,
            client_input, client_type_select, contact_input, product_type_input, status_select,
            select_files_btn, selected_files_text,
            create_btn, update_btn]
