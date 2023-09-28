filters = [
    "*://googleads.g.doubleclick.net/*"
]
chrome.webRequest.onBeforeRequest.addListener(
    function (details) {
        return{cancel: true}
    },
    {urls: filters},
    ["blocking"]
)

