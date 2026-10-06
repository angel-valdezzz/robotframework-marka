*** Settings ***
Library    SeleniumLibrary
Library    Marka
Variables    browser_options.py
Suite Teardown    Close All Browsers

*** Variables ***
${BROWSER}    chrome

*** Test Cases ***
Annotate A Screenshot
    Open Browser    file://${CURDIR}/page.html    ${BROWSER}    options=${CHROME_OPTIONS}    service=${CHROME_SERVICE}
    Set Window Size    1100    800
    Highlight Element    id:email    background=rgba(240,100,69,0.12)    group=profile
    Add Dot    id:email    text=1    position=left    group=profile
    Add Note    id:save    text=Save the updated profile    position=right    group=profile
    Click Element    id:save
    Element Text Should Be    id:result    Saved
    Capture Annotated Screenshot    ${OUTPUT DIR}/annotated.png
    ${removed}=    Clear Annotations
    Should Be Equal As Integers    ${removed}    0
