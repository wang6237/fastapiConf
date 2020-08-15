import request from '@/utils/request'

export function getEnvLists() {
  return request({
    url: '/v1/env/',
    method: 'get'
  })
}

export function addEnvList(data) {
  return request({
    url: '/v1/env/',
    method: 'post',
    data
  })
}

export function editEnvList(data) {
  return request({
    // url: '/v1/env/'+id +'/' + template_name,
    url: '/v1/env/',
    method: 'put',
    data
  })
}

export function delEnvList(id) {
  return request({
    url: '/v1/env/' + id,
    method: 'delete'
    // params: { name }
  })
}

export function syncEtcd(data) {
  return request({
    url: '/v1/env/sync/',
    method: 'post',
    data
  })
}

export function syncEtcdDelete(envId, data) {
  return request({
    url: '/v1/env/sync/' + envId,
    method: 'delete',
    data
  })
}

export function syncState(envId, data) {
  return request({
    url: '/v1/env/sync/state/' + envId,
    method: 'put',
    data
  })
}

export function getEtcdData(data) {
  return request({
    url: '/v1/env/get_etcd/',
    method: 'post',
    data
  })
}

export function updateEtcdData(envId, data) {
  return request({
    url: '/v1/env/update_etcd/' + envId,
    method: 'put',
    data
  })
}
