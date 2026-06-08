-- Create Users Table

CREATE TABLE users (
    visitor_id BIGINT PRIMARY KEY
);

-- Create Items Table

CREATE TABLE items (
    item_id BIGINT PRIMARY KEY
);

-- Create Interactions Table

CREATE TABLE interactions (
    interaction_id INT AUTO_INCREMENT PRIMARY KEY,

    visitor_id BIGINT NOT NULL,

    item_id BIGINT NOT NULL,

    interaction_strength INT,

    recency_days INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (visitor_id)
    REFERENCES users(visitor_id),

    FOREIGN KEY (item_id)
    REFERENCES items(item_id)
);