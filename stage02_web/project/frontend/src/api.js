async function request(path, options = {}) {
  const response = await fetch(`/api${path}`, options)
  if (!response.ok) {
    throw new Error(`请求失败：HTTP ${response.status}`)
  }
  if (response.status === 204) return null
  return response.json()
}

export const listTasks = () => request('/tasks')
export const createTask = (title) =>
  request('/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  })
export const updateTask = (id, done) =>
  request(`/tasks/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ done }),
  })
export const deleteTask = (id) => request(`/tasks/${id}`, { method: 'DELETE' })
