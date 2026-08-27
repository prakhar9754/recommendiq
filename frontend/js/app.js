/* =========================================================
   RecommendIQ Frontend
========================================================= */


/* ========================================================
   CURRENT CUSTOMER
======================================================== */

let currentVisitorId = null;


/* ========================================================
   MOBILE SIDEBAR
======================================================== */

const mobileMenu = document.getElementById("mobileMenu");
const sidebar = document.getElementById("sidebar");

if (mobileMenu && sidebar) {

    mobileMenu.addEventListener("click", () => {

        sidebar.classList.toggle("open");

    });

}


/* ========================================================
   NAVIGATION
======================================================== */

const navItems = document.querySelectorAll(".nav-item");

navItems.forEach((item) => {

    item.addEventListener("click", function (event) {

        event.preventDefault();

        navItems.forEach((nav) => {

            nav.classList.remove("active");

        });

        this.classList.add("active");

        const page = this.dataset.page;

        console.log("Selected page:", page);

    });

});


/* ========================================================
   QUICK ACTIONS
======================================================== */

const quickActions =
    document.querySelectorAll(".quick-action");

quickActions.forEach((button) => {

    button.addEventListener("click", () => {

        console.log(
            "Quick action clicked:",
            button.innerText
        );

    });

});


/* ========================================================
   GENERATE INSIGHTS BUTTON
======================================================== */

const generateButton =
    document.querySelector(".primary-button");

if (generateButton) {

    generateButton.addEventListener("click", () => {

        generateButton.innerHTML = `
            <span>✓</span>
            Insights Ready
        `;

        setTimeout(() => {

            generateButton.innerHTML = `
                <span>✦</span>
                Generate Insights
            `;

        }, 2000);

    });

}


/* ========================================================
   CONSOLE MESSAGE
======================================================== */

console.log(
    "RecommendIQ frontend loaded successfully."
);


/* ========================================================
   FASTAPI CONNECTION
======================================================== */

const API_BASE_URL = "http://127.0.0.1:8000";


/* ========================================================
   TEST FASTAPI CONNECTION
======================================================== */

async function testAPI() {

    try {

        const response = await fetch(
            `${API_BASE_URL}/`
        );

        if (!response.ok) {

            throw new Error(
                `API Error: ${response.status}`
            );

        }

        const data = await response.json();

        console.log(
            "FastAPI connection successful."
        );

        console.log(
            "API Response:",
            data
        );

    } catch (error) {

        console.error(
            "FastAPI connection failed:",
            error
        );

    }

}


/* ========================================================
   GET CUSTOMER SEGMENT
======================================================== */

async function getCustomerSegment(visitorId) {

    try {

        const response = await fetch(
            `${API_BASE_URL}/segment/${visitorId}`
        );

        if (!response.ok) {

            throw new Error(
                `API Error: ${response.status}`
            );

        }

        const data = await response.json();

        console.log(
            "Customer Segment:",
            data
        );

        return data;

    } catch (error) {

        console.error(
            "Error fetching customer segment:",
            error
        );

        return null;

    }

}


/* ========================================================
   GET CUSTOMER RECOMMENDATIONS
======================================================== */

async function getRecommendations(visitorId) {

    try {

        const response = await fetch(
            `${API_BASE_URL}/recommend/${visitorId}`
        );

        if (!response.ok) {

            throw new Error(
                `API Error: ${response.status}`
            );

        }

        const data = await response.json();

        console.log(
            "Customer Recommendations:",
            data
        );

        return data;

    } catch (error) {

        console.error(
            "Error fetching recommendations:",
            error
        );

        return null;

    }

}


/* ========================================================
   CUSTOMER SEARCH
======================================================== */

const visitorIdInput =
    document.getElementById("visitorIdInput");

const searchCustomerButton =
    document.getElementById("searchCustomerButton");

const customerSegment =
    document.getElementById("customerSegment");


if (
    visitorIdInput &&
    searchCustomerButton
) {

    searchCustomerButton.addEventListener(
        "click",
        async () => {

            const visitorId =
                visitorIdInput.value.trim();


            /* Save current customer */

            currentVisitorId = visitorId;


            /* Check Visitor ID */

            if (!visitorId) {

                alert(
                    "Please enter a Visitor ID."
                );

                return;

            }


            /* Loading state */

            searchCustomerButton.innerHTML = `
                <span>⟳</span>
                Searching...
            `;


            try {

                console.log(
                    "Searching customer:",
                    visitorId
                );


                /* =========================================
                   GET CUSTOMER SEGMENT
                ========================================= */

                const segmentData =
                    await getCustomerSegment(
                        visitorId
                    );


                console.log(
                    "Customer data:",
                    segmentData
                );


                if (!segmentData) {

                    throw new Error(
                        "Customer not found."
                    );

                }


                /* Display customer segment */

                if (customerSegment) {

                    customerSegment.innerText =
                        segmentData.customer_segment ||
                        segmentData.segment ||
                        "Unknown";

                }


                /* =========================================
                   GET RECOMMENDATIONS
                ========================================= */

                const recommendationData =
                    await getRecommendations(
                        visitorId
                    );


                console.log(
                    "Recommendation data:",
                    recommendationData
                );


                /* Display recommendations */

                displayRecommendations(
                    recommendationData
                );

            } catch (error) {

                console.error(
                    "Customer search failed:",
                    error
                );


                /* Display error */

                if (customerSegment) {

                    customerSegment.innerText =
                        "Not Found";

                }


                /* Clear recommendations */

                displayRecommendations(null);

            }


            /* Restore button */

            searchCustomerButton.innerHTML = `
                <span>⌕</span>
                Search Customer
            `;

        }
    );

}


/* ========================================================
   DISPLAY RECOMMENDATIONS
======================================================== */

function displayRecommendations(data) {

    const recommendationGrid =
        document.getElementById(
            "recommendationGrid"
        );

    const recommendationStatus =
        document.getElementById(
            "recommendationStatus"
        );


    /* Check recommendation container */

    if (!recommendationGrid) {

        return;

    }


    /* Clear previous recommendations */

    recommendationGrid.innerHTML = "";


    /* ====================================================
       HANDLE EMPTY RESPONSE
    ==================================================== */

    if (!data) {

        recommendationGrid.innerHTML = `
            <div class="recommendation-empty">

                <div class="empty-icon">
                    !
                </div>

                <h4>
                    No Recommendations Found
                </h4>

                <p>
                    We could not generate recommendations
                    for this customer.
                </p>

            </div>
        `;


        if (recommendationStatus) {

            recommendationStatus.innerText =
                "0 items found";

        }


        return;

    }


    /* ====================================================
       GET RECOMMENDATION LIST
    ==================================================== */

    const recommendations =
        data.recommendations ||
        data.items ||
        data;


    /* ====================================================
       CHECK RECOMMENDATIONS
    ==================================================== */

    if (
        !Array.isArray(recommendations) ||
        recommendations.length === 0
    ) {

        recommendationGrid.innerHTML = `
            <div class="recommendation-empty">

                <div class="empty-icon">
                    !
                </div>

                <h4>
                    No Recommendations Available
                </h4>

                <p>
                    There are no recommendations
                    available for this customer.
                </p>

            </div>
        `;


        if (recommendationStatus) {

            recommendationStatus.innerText =
                "0 items found";

        }


        return;

    }


    /* ====================================================
       UPDATE RECOMMENDATION COUNT
    ==================================================== */

    if (recommendationStatus) {

        recommendationStatus.innerText =
            `${recommendations.length} items found`;

    }


    /* ====================================================
       CREATE RECOMMENDATION CARDS
    ==================================================== */

    recommendations.forEach(
        (item, index) => {

            /* Get item ID */

            const itemId =
                typeof item === "object"
                    ? item.itemid
                    : item;


            /* Create card */

            const card =
                document.createElement("div");


            card.className =
                "recommendation-card";


            /* =================================================
               RECOMMENDATION SCORE
            ================================================= */

            const score =
                typeof item === "object"
                    ? item.recommendation_score
                    : null;


            let scorePercentage = null;


            if (
                score !== null &&
                score !== undefined &&
                !isNaN(Number(score))
            ) {

                scorePercentage =
                    Math.round(
                        Number(score) * 100
                    );

            }


            /* Score display */

            const scoreDisplay =
                scorePercentage !== null
                    ? `${scorePercentage}%`
                    : "AI";


            /* =================================================
               CARD HTML
            ================================================= */

            card.innerHTML = `

                <div class="recommendation-image">

                    <span class="recommendation-icon">
                        ✦
                    </span>

                    <span class="recommendation-rank">
                        #${index + 1}
                    </span>

                </div>


                <div class="recommendation-content">

                    <div class="recommendation-top">

                        <span class="recommendation-label">
                            AI PICK
                        </span>

                        <span class="recommendation-score">
                            ${scoreDisplay}
                        </span>

                    </div>


                    <h4>
                        Product ${itemId}
                    </h4>


                    <p>
                        Recommended based on
                        customer behavior
                    </p>


                    <div class="score-container">

                        <div class="score-bar">

                            <div
                                class="score-progress"
                                style="width: ${
                                    scorePercentage !== null
                                        ? scorePercentage
                                        : 85
                                }%"
                            ></div>

                        </div>

                    </div>


                    <div class="recommendation-footer">

                        <span>
                            ✦ Personalized
                        </span>

                        <button
                            class="view-product-button"
                            type="button"
                        >
                            View
                        </button>

                    </div>

                </div>

            `;


            /* =================================================
               ADD CARD TO PAGE
            ================================================= */

            recommendationGrid.appendChild(
                card
            );


            /* =================================================
               VIEW PRODUCT BUTTON
            ================================================= */

            const viewButton =
                card.querySelector(
                    ".view-product-button"
                );


            if (viewButton) {

                viewButton.addEventListener(
                    "click",
                    () => {

                        console.log(
                            "Selected product:",
                            itemId
                        );

                        alert(
                            `Product ${itemId} selected`
                        );

                    }
                );

            }

        }
    );

}


/* ========================================================
   RUN API CONNECTION TEST
======================================================== */

testAPI();