"""
RVPresentationDocument
    @height
    @width
    @docType
    @versionNumber
    @usedCount
    @backgroundColor
    @drawingBackgroundColor
    @CCLIDisplay
    @lastDateUsed
    @selectedArrangementID
    @category
    @resourcesDirectory
    @notes
    @CCLIAuthor
    @CCLIArtistCredits
    @CCLISongTitle
    @CCLIPublisher
    @CCLICopyrightYear
    @CCLISongNumber
    @chordChartPath
    @os
    @buildNumber

    RVTimeline
        @timeOffset
        @duration
        @selectedMediaTrackIndex
        @loop

        array[timeCues]
        array[mediaTracks]

    array[groups]
        RVSlideGrouping - array[slides]
        LOWERCASE UUID

    array[arrangements]
        RVSongArrangement
            @name
            @color
            @uuid (LOWERCASE)
            array
                array[NSString]


"""
