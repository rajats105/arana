var require = patchRequire(require)

var host_wait = {
  'www.shine.com': 'div.search_listingleft a span.snp_yoe_loc em.snp_loc',
  'www.naukri.com': 'div.row[type=tuple]'
}

var host_next = {
  'www.shine.com': [
    'input.cls_paginate.submit[data-type=next]'
  ],
  'www.naukri.com': [
    'div.pagination > a:nth-child(2) > button',
    'div.pagination > a > button'
  ]
}

// exports.exit_codes = {
//   'success': 0,
//   'invalidUrl': 2,
//   'storageIssue': 3,
//   'waitTimeout': 4
// }

/**
 * Extract domain name
 */
function extractHost (url) {
  var domain

  // find & remove protocol (http, ftp, etc.) and get domain
  if (url.indexOf('://') > -1) {
    domain = url.split('/')[2]
  } else {
    domain = url.split('/')[0]
  }

  // find & remove port number
  return domain.split(':')[0]
}

/**
 * Validate crawling
 */
function validateCrawl (url) {
  var host = extractHost(url)

  if (host_wait.hasOwnProperty(host) && host_next.hasOwnProperty(host)) {
    return true
  }

  return false
}

function parseKeyInOptions (key, options, def) {
  // https://stackoverflow.com/questions/1098040/checking-if-a-key-exists-in-a-javascript-object
  def = typeof def !== 'undefined' ? def : false

  if (options.hasOwnProperty(key)) {
    return options[key]
  }

  return def
}

exports.parseKeyInOptions = parseKeyInOptions

exports.getWaitSelector = function getWaitSelector (host) {
  return host_wait[host]
}

exports.getNextButtonSelector = function getNextButtonSelector (host) {
  return host_next[host]
}

exports.getCrawlHost = function getCrawlHost (url) {
  return extractHost(url)
}

exports.parseCrawlUrl = function parseCrawlUrl (options) {
  var url = parseKeyInOptions('url', options)

  if (validateCrawl(url)) {
    return options.url
  }

  return false
}