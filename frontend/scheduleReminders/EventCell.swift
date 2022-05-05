//
//  EventCell.swift
//  scheduleReminders
//
//  Created by Dylan Van Bramer on 5/1/22.
//

import Foundation
import UIKit

class EventCell: UITableViewCell {
    
    static let id = "EventCellId"
    
    let title: UILabel = {
        let label = UILabel()
        label.textColor = .black
        label.font = .systemFont(ofSize: 15, weight: .black)
        label.translatesAutoresizingMaskIntoConstraints = false
        label.textAlignment = .left
        label.text = "Calendar Event"
        return label
    }()
    
    
    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        layer.borderColor = UIColor.darkGray.cgColor
        backgroundColor = .lightGray
       
        addSubview(title)
        
        
        NSLayoutConstraint.activate([
            title.leadingAnchor.constraint(equalTo: leadingAnchor),
            title.topAnchor.constraint(equalTo: topAnchor),
            title.trailingAnchor.constraint(equalTo: trailingAnchor),
            title.heightAnchor.constraint(equalToConstant: 15),
        ])
    }
    required init?(coder: NSCoder) {
            fatalError("init(coder:) has not been implemented")
    }
    
    func populateCell(event: Event){
        title.text = event.title
    }
    // implement this when populating a cell with its new calendar information
}
