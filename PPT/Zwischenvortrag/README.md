AISEC Beamer Theme
==================

## Included Files

    aisec_building.pdf      Picture of the Business Campus building
    aisec_logo.pdf          Fraunhofer AISEC logo
    beamer*themeAISEC.sty   Theme style files
    presentation.pdf        Compiled example
    presentation.tex        Example TEX file
    README                  This readme file

## Using the Theme

The theme has to be loaded at the beginning of the preamble with the
`\usetheme{AISEC}` command. The presentation can then be compiled with
`pdflatex presentation.tex`.

The theme also uses the Fraunhofer font Frutiger, which has to be installed
and then be loaded with `\usepackage{fhgfont}`. The font can be obtained from:
<https://intrawiki.aisec.fraunhofer.de/pub/Main/DokumentVorlagen/fhg_frutiger_tex.zip>

## Fraunhofer Colors

The theme defines the following official Fraunhofer colors. They can be used
with `\color{foo}`:

    fraunhofergreen
    fraunhofergrey
    fraunhoferorange
    fraunhofernavy
    fraunhofercyan
    fraunhoferlime
    fraunhoferlightbeige
    fraunhoferlightblue
    fraunhoferlightgrey

## New Options

## Infoline

Default: _Enabled_
Command: Use `\infolinefalse` to disable

By default, the theme displays a infoline in the footer of each slide. The
infoline consists of the shortened title, the shortened author list, the date
and the current slide number.

## Numbering

Default: _Disabled_
Command: Use `\numberingtrue` to enable

With this theme it is possible to use latex sectioning to automatically set
the titles and subtitles of slides, as well as populating the outline of the
presentation. If numbering is enabled, the titles and subtitles will have the
correct section numbers shown.

Besides using sectioning it is still possible to set titles and subtitles
manually using `\frametitle{}` and `\framesubtitle{}`.

## Square Bullet Points

Default: _Enabled_
Command: Use `\squaresfalse` to disable

The theme uses square bullet points in itemize environments, as suggested by
Fraunhofer. Disabling this option will set them back to triangles.

## Extended title page

Default: _Enabled_
Command: Use `\extendedtitlefalse` to disable

By default, the theme uses the Fraunhofer title page format, where title,
subtitle, the list of authors and the date are shown between two green rules.
To only show the title between those rules, disable this option. The rest of
the title page can be modified by the user (e.g. the title page image).

## Confidential

Default: _Disabled_
Command: Use `\confidentialtrue` to enable

This option will enable the display of a red CONFIDENTIAL string in the
infoline (in the footer) of each slide. The option infoline has to be enabled.

## New Environments

Because the theme uses different styles for headlines, some additional
environments have been defined to create certain frames. These environments
extend Beamer's frame environment and thus can be used with the usual options
for frames (e.g. `\begin{bibliographypage}[t]` for vertical top alignment).

## Title Frame

This environment is used to create a title frame. Within this frame the title
page can be automatically generated using the command `\titlepage`. The
`\titlepage` command uses the macros stated below. The logo is not part of the
automatic title page generation, because then it's much easier to alter it
manually.

    \title{}        The title of the presentation.
    \subtitle{}     The subtitle of the presentation. Setting this macro is
                    optional.
    \author{}       The author list.
    \date{}         The date. May be \today.

With `\extendedtitlefalse` set, the macros subtitle, author and date are not
used by the `\titlepage` command.

**Example**:

    \begin{titleframe}
        \titlepage
    \end{titleframe}

## Outline frame

This environment is used to create an outline frame. By default, the
outline frame contains the presentation's title as frame title. To change
the frame title use `\frametitle{}`. Options to the `\tableofcontents`
command still work as expected.

**Example**:

    \begin{outlineframe}
        \tableofcontents
    \end{outlineframe}

## Bibliography frame

This environment is used to create a bibliography frame with the title
"Bibliography". Again, change it using `\frametitle{}`.

## Contact frame

This environment is used to create a contact information frame with the title
"Contact Information". Use `\contactpage` to create the contact information.
The macros stated below may be used to create the contact information. All
macros are optional and can be left blank, if needed.

    \name{}         Your name. May be \insertauthor from the title page.
    \department{}   Your group, department or both.
    \institute{}    The institute's name.
    \address{}      The institute's address.
    \web{}          The URL to the website.
    \phone{}        Your phone number.
    \fax{}          Your fax number.
    \email{}        Your email address.

**Example**:

    \begin{contactframe}
        \contactpage
    \end{contactframe}

