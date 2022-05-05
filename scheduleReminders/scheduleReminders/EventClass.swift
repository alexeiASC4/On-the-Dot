//
//  EventClass.swift
//  scheduleReminders
//
//  Created by Dylan Van Bramer on 5/1/22.
//

import Foundation
import UIKit

//definitely doesn't need to be its own file
//where else should I put this?

struct Event {
    var id: UUID?
    var title: String?
    var startTime: Date?
    var duration: Date?
    
}
//don't know which to use for dateTime events??

var eventList: [Event] = []
