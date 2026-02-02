// === Cambia estas URLs según Docker o Kubernetes ===
// Docker Compose:
// const URL_PRODUCTOS = "http://localhost:8000";
// const URL_ORDENES   = "http://localhost:8001";

// Kubernetes con minikube service (te dará URLs dinámicas):
// pega aquí lo que te salga en consola o usa Ingress si quieres fijo.
const URL_PRODUCTOS = "http://localhost:8000";
const URL_ORDENES   = "http://localhost:8001";


const $ = (id) => document.getElementById(id);

function renderTablaProductos(items) {
  if (!items.length) return "<p><small>No hay productos.</small></p>";
  const rows = items.map(p => `
    <tr>
      <td>${p.id}</td>
      <td>${p.nombre}</td>
      <td>${p.precio}</td>
      <td>${p.stock}</td>
    </tr>
  `).join("");
  return `
    <table>
      <thead><tr><th>ID</th><th>Nombre</th><th>Precio</th><th>Stock</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

function renderTablaOrdenes(items) {
  if (!items.length) return "<p><small>No hay órdenes.</small></p>";
  const rows = items.map(o => `
    <tr>
      <td>${o.id}</td>
      <td>${o.producto_id} - ${o.producto_nombre}</td>
      <td>${o.precio_unitario}</td>
      <td>${o.cantidad}</td>
      <td>${o.total}</td>
      <td>${o.estado}</td>
    </tr>
  `).join("");
  return `
    <table>
      <thead><tr><th>ID</th><th>Producto</th><th>Precio</th><th>Cant.</th><th>Total</th><th>Estado</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

async function cargarProductos() {
  const r = await fetch(`${URL_PRODUCTOS}/productos`);
  const data = await r.json();
  $("tablaProductos").innerHTML = renderTablaProductos(data);
}

async function cargarOrdenes() {
  const r = await fetch(`${URL_ORDENES}/ordenes`);
  const data = await r.json();
  $("tablaOrdenes").innerHTML = renderTablaOrdenes(data);
}

$("btnCrearProducto").onclick = async () => {
  $("msgProducto").textContent = "";
  try {
    const payload = {
      nombre: $("nombre").value.trim(),
      precio: Number($("precio").value),
      stock: Number($("stock").value),
    };
    const r = await fetch(`${URL_PRODUCTOS}/productos`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || "Error creando producto");
    $("msgProducto").innerHTML = `<span class="ok">Producto creado: ID ${data.id}</span>`;
    await cargarProductos();
  } catch (e) {
    $("msgProducto").innerHTML = `<span class="error">${e.message}</span>`;
  }
};

$("btnCrearOrden").onclick = async () => {
  $("msgOrden").textContent = "";
  try {
    const payload = {
      producto_id: Number($("producto_id").value),
      cantidad: Number($("cantidad").value),
    };
    const r = await fetch(`${URL_ORDENES}/ordenes`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || "Error creando orden");
    $("msgOrden").innerHTML = `<span class="ok">Orden creada: ID ${data.id} (Total ${data.total})</span>`;
    await cargarOrdenes();
    await cargarProductos(); // porque baja stock
  } catch (e) {
    $("msgOrden").innerHTML = `<span class="error">${e.message}</span>`;
  }
};

$("btnRefrescarProductos").onclick = cargarProductos;
$("btnRefrescarOrdenes").onclick = cargarOrdenes;

// carga inicial
cargarProductos();
cargarOrdenes();
