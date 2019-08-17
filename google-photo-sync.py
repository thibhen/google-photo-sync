

import requests,json,os,datetime

____bearer___ = "Bearer ya29.GmRnB9dAVkSM8mMccSJCSvn-p-cQ1S1T7yzhUXV6yplvGekY1kZ7cNQg0aRSCr5OnxRDXOLrLwmQOCK0D_Vkw_qZk2ytJXt9FPnpfGcIdM8Sl0QS6d-D9mobunwSRhkZxrkIzlCq"
____album_to_download___ = "backup"

# Login
# TODO
# scope = "https://www.googleapis.com/auth/photoslibrary.readonly"


# Identify the Album ID // ?key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM
albumId = None
with requests.get('https://content-photoslibrary.googleapis.com/v1/albums',
        headers={
            "x-referer": "https://explorer.apis.google.com",
            "authorization": ____bearer___ 
        }) as response:
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    for album in response.json()["albums"]:
        print("INFO : {} --- {}".format(album["title"],album["productUrl"]))
        
        if album["title"] == ____album_to_download___ :
            albumId = album["id"]

# List Photos to be downloaded
pageToken = None

# TODO : decrement iPage
with requests.post('https://photoslibrary.googleapis.com/v1/mediaItems:search',
        headers={
            "x-referer": "https://explorer.apis.google.com",
            "authorization": ____bearer___
        },
        data={
            "pageSize": "100",
            "pageToken":pageToken,
            "albumId": albumId
        }) as response:
    
    print("INFO : Http code {}".format(response.status_code))
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    
    if "nextPageToken" not in response.json():
        break
    
    pageToken = response.json()["nextPageToken"]
    iPage = iPage - 1

    for mediaItem in response.json()["mediaItems"] :
        (year,month,*x) = mediaItem["mediaMetadata"]["creationTime"].split("-")
        
        # baseUrl = "{}=w{}-h{}".format(
        #            mediaItem["baseUrl"],
        #            mediaItem["mediaMetadata"]["width"],
        #            mediaItem["mediaMetadata"]["height"])

        if "video" in mediaItem["mediaMetadata"].keys(): # video
            baseUrl = "{}=dv".format(mediaItem["baseUrl"])
            targetFolder = "download/video/{}-{}".format(year,month)
        else: # Photo
            baseUrl = "{}=d".format(mediaItem["baseUrl"])
            targetFolder = "download/photo/{}-{}".format(year,month)

        targetFile = "{}/{}".format(targetFolder,mediaItem["filename"])
                
        print("INFO : {} <===> {}".format(targetFile,baseUrl))

        if not os.path.exists(targetFolder):
            os.makedirs(targetFolder)

        if (not os.path.exists(targetFile)):
            with open(targetFile, 'wb') as f:
                f.write(requests.get(baseUrl).content)

                fileTime = datetime.datetime.strptime(
                    mediaItem["mediaMetadata"]["creationTime"], '%Y-%m-%dT%H:%M:%SZ') # "2019-04-18T13:07:30Z"
                fileTimeInt = int(fileTime.strftime('%Y%m%d'))
                os.utime(targetFile, (fileTimeInt, fileTimeInt))
        else:
            print("WARN : Skipping {}".format(targetFile))

