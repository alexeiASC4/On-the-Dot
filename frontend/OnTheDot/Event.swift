//
//  Event.swift
//  OnTheDot
//
//  Created by Kyle Betts on 2022-05-05.
//

class Event {
    let id: String
    let name: String
    let datetime: Int
    let duration: Int
    let location: String
    let arrival: Int
    let user: Int
    
    init(id: String, name: String, datetime: Int, duration: Int, location: String, arrival: Int, user: Int) {
        self.id = id
        self.name = name
        self.datetime = datetime
        self.duration = duration
        self.location = location
        self.arrival = arrival
        self.user = user
    }
    
}
