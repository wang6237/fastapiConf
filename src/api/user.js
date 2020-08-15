import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'v1/user/login',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: 'v1/user/info',
    method: 'get'
    // params: { token }
  })
}

export function getMenu() {
  return request({
    url: 'v1/user/menu/',
    method: 'get',
    // params: { userId }
  })
}

export function getUserListInfo() {
  return request({
    url: 'v1/user/',
    method: 'get'
    // params: { token }
  })
}

export function createUser(data) {
  return request({
    url: 'v1/user/',
    method: 'post',
    data
    // params: { token }
  })
}

export function updateUser(data) {
  return request({
    url: 'v1/user/',
    method: 'put',
    data
    // params: { token }
  })
}

export function deleteUser(username) {
  return request({
    url: 'v1/user/',
    method: 'delete',
    // data
    params: { username }
  })
}

export function logout(data) {
  return request({
    url: 'v1/user/logout',
    method: 'post',
    data
  })
}
