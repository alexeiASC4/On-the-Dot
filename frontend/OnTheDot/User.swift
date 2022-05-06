//
//  User.swift
//  OnTheDot
//
//  Created by Kyle Betts on 2022-05-05.
//

class User {
    let sessionToken: String
    let sessionExpiration: String
    let updateToken: String
    
    init(sessionToken: String, sessionExpiration: String, updateToken: String) {
        self.sessionToken = sessionToken
        self.sessionExpiration = sessionExpiration
        self.updateToken = updateToken
    }
}
