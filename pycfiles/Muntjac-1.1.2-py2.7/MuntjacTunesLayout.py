# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/MuntjacTunesLayout.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Application
from muntjac.terminal.sizeable import ISizeable
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.ui.window import Notification
from muntjac.api import Alignment, ComboBox, Embedded, HorizontalLayout, HorizontalSplitPanel, Label, NativeButton, NativeSelect, Slider, Table, VerticalLayout, Window

class MuntjacTunesLayout(Application):
    """Sample application layout, similar (almost identical) to Apple iTunes.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    def init(self):
        rootLayout = VerticalLayout()
        root = Window('MuntjacTunes', rootLayout)
        self.setMainWindow(root)
        root.showNotification('This is an example of how you can do layouts in Muntjac.<br/>It is not a working sound player.', Notification.TYPE_HUMANIZED_MESSAGE)
        rootLayout.setSizeFull()
        rootLayout.setMargin(False)
        top = HorizontalLayout()
        top.setWidth('100%')
        top.setMargin(False, True, False, True)
        top.setSpacing(True)
        root.addComponent(top)
        playback = HorizontalLayout()
        volume = HorizontalLayout()
        status = HorizontalLayout()
        viewmodes = HorizontalLayout()
        search = ComboBox()
        top.addComponent(playback)
        top.addComponent(volume)
        top.addComponent(status)
        top.addComponent(viewmodes)
        top.addComponent(search)
        top.setComponentAlignment(playback, Alignment.MIDDLE_LEFT)
        top.setComponentAlignment(volume, Alignment.MIDDLE_LEFT)
        top.setComponentAlignment(status, Alignment.MIDDLE_CENTER)
        top.setComponentAlignment(viewmodes, Alignment.MIDDLE_LEFT)
        top.setComponentAlignment(search, Alignment.MIDDLE_LEFT)
        top.setExpandRatio(status, 1.0)
        prev = NativeButton('Previous')
        play = NativeButton('Play/pause')
        nextt = NativeButton('Next')
        playback.addComponent(prev)
        playback.addComponent(play)
        playback.addComponent(nextt)
        playback.setSpacing(True)
        mute = NativeButton('mute')
        vol = Slider()
        vol.setOrientation(Slider.ORIENTATION_HORIZONTAL)
        vol.setWidth('100px')
        maxx = NativeButton('max')
        volume.addComponent(mute)
        volume.addComponent(vol)
        volume.addComponent(maxx)
        status.setWidth('80%')
        status.setSpacing(True)
        toggleVisualization = NativeButton('Mode')
        timeFromStart = Label('0:00')
        trackDetails = VerticalLayout()
        trackDetails.setWidth('100%')
        track = Label('Track Name')
        album = Label('Album Name - Artist')
        track.setWidth(None)
        album.setWidth(None)
        progress = Slider()
        progress.setOrientation(Slider.ORIENTATION_HORIZONTAL)
        progress.setWidth('100%')
        trackDetails.addComponent(track)
        trackDetails.addComponent(album)
        trackDetails.addComponent(progress)
        trackDetails.setComponentAlignment(track, Alignment.TOP_CENTER)
        trackDetails.setComponentAlignment(album, Alignment.TOP_CENTER)
        timeToEnd = Label('-4:46')
        jumpToTrack = NativeButton('Show')
        status.addComponent(toggleVisualization)
        status.setComponentAlignment(toggleVisualization, Alignment.MIDDLE_LEFT)
        status.addComponent(timeFromStart)
        status.setComponentAlignment(timeFromStart, Alignment.BOTTOM_LEFT)
        status.addComponent(trackDetails)
        status.addComponent(timeToEnd)
        status.setComponentAlignment(timeToEnd, Alignment.BOTTOM_LEFT)
        status.addComponent(jumpToTrack)
        status.setComponentAlignment(jumpToTrack, Alignment.MIDDLE_LEFT)
        status.setExpandRatio(trackDetails, 1.0)
        viewAsTable = NativeButton('Table')
        viewAsGrid = NativeButton('Grid')
        coverflow = NativeButton('Coverflow')
        viewmodes.addComponent(viewAsTable)
        viewmodes.addComponent(viewAsGrid)
        viewmodes.addComponent(coverflow)
        bottom = HorizontalSplitPanel()
        root.addComponent(bottom)
        root.getContent().setExpandRatio(bottom, 1.0)
        bottom.setSplitPosition(200, ISizeable.UNITS_PIXELS)
        sidebar = VerticalLayout()
        sidebar.setSizeFull()
        bottom.setFirstComponent(sidebar)
        selections = VerticalLayout()
        library = Label('Library')
        music = NativeButton('Music')
        music.setWidth('100%')
        store = Label('Store')
        muntjacTunesStore = NativeButton('MuntjacTunes Store')
        muntjacTunesStore.setWidth('100%')
        purchased = NativeButton('Purchased')
        purchased.setWidth('100%')
        playlists = Label('Playlists')
        genius = NativeButton('Geniues')
        genius.setWidth('100%')
        recent = NativeButton('Recently Added')
        recent.setWidth('100%')
        selections.addComponent(library)
        selections.addComponent(music)
        selections.addComponent(store)
        selections.addComponent(muntjacTunesStore)
        selections.addComponent(purchased)
        selections.addComponent(playlists)
        selections.addComponent(genius)
        selections.addComponent(recent)
        sidebar.addComponent(selections)
        sidebar.setExpandRatio(selections, 1.0)
        cover = Embedded('Currently Playing')
        sidebar.addComponent(cover)
        listing = Table()
        listing.setSizeFull()
        listing.setSelectable(True)
        bottom.setSecondComponent(listing)
        listing.addContainerProperty('Name', str, '')
        listing.addContainerProperty('Time', str, '0:00')
        listing.addContainerProperty('Artist', str, '')
        listing.addContainerProperty('Album', str, '')
        listing.addContainerProperty('Genre', str, '')
        listing.addContainerProperty('Rating', NativeSelect, NativeSelect())
        tracks = [
         'Red Flag', 'Millstone', 'Not The Sun', 'Breath',
         'Here We Are', 'Deep Heaven', 'Her Voice Resides',
         'Natural Tan', 'End It All', 'Kings', 'Daylight Slaving',
         'Mad Man', 'Resolve', 'Teargas', 'African Air', 'Passing Bird']
        times = ['4:12', '6:03', '5:43', '4:32', '3:42', '4:45', '2:56',
         '9:34', '2:10', '3:44', '5:49', '6:30', '5:18', '7:42',
         '3:13', '2:52']
        artists = ['Billy Talent', 'Brand New', 'Breaking Benjamin',
         'Becoming The Archetype', 'Bullet For My Valentine',
         'Chasing Victory', 'Chimaira', 'Danko Jones', 'Deadlock',
         'Deftones', 'From Autumn To Ashes', 'Haste The Day',
         'Four Year Strong', 'In Flames', 'Kemopetrol', 'John Legend']
        albums = ['Once Again', 'The Caitiff Choir', 'The Devil And God',
         'Light Grenades', 'Dicthonomy', 'Back In Black', 'Dreamer',
         'Come Clarity', 'Year Zero', 'Frames', 'Fortress', 'Phobia',
         'The Poison', 'Manifesto', 'White Pony', 'The Big Dirty']
        genres = ['Rock', 'Metal', 'Hardcore', 'Indie', 'Pop', 'Alternative',
         'Blues', 'Jazz', 'Hip Hop', 'Electronica', 'Punk', 'Hard Rock',
         'Dance', "R'n'B", 'Gospel', 'Country']
        for i in range(100):
            s = NativeSelect()
            s.addItem('1 star')
            s.addItem('2 stars')
            s.addItem('3 stars')
            s.addItem('4 stars')
            s.addItem('5 stars')
            s.select('%d stars' % (i % 5))
            index = i % 16
            listing.addItem([tracks[index], times[index],
             artists[index], albums[index], genres[index], s], i)

        listing.setColumnAlignment('Time', Table.ALIGN_RIGHT)
        self.setTheme('vaadintunes')
        root.setStyleName('tTunes')
        top.setStyleName('top')
        top.setHeight('75px')
        playback.setStyleName('playback')
        playback.setMargin(False, True, False, False)
        play.setStyleName('play')
        nextt.setStyleName('next')
        prev.setStyleName('prev')
        playback.setComponentAlignment(prev, Alignment.MIDDLE_LEFT)
        playback.setComponentAlignment(nextt, Alignment.MIDDLE_LEFT)
        volume.setStyleName('volume')
        mute.setStyleName('mute')
        maxx.setStyleName('max')
        vol.setWidth('78px')
        status.setStyleName('status')
        status.setMargin(True)
        status.setHeight('46px')
        toggleVisualization.setStyleName('toggle-vis')
        jumpToTrack.setStyleName('jump')
        viewAsTable.setStyleName('viewmode-table')
        viewAsGrid.setStyleName('viewmode-grid')
        coverflow.setStyleName('viewmode-coverflow')
        sidebar.setStyleName('sidebar')
        music.setStyleName('selected')
        cover.setSource(ThemeResource('images/album-cover.jpg'))
        cover.setWidth('100%')
        return


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(MuntjacTunesLayout, nogui=True, forever=True, debug=True)